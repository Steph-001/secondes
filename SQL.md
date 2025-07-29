
-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop existing table if it exists to recreate with proper constraints
DROP TABLE IF EXISTS public.flashcard_progress CASCADE;

-- Create flashcard_progress table with strict constraints
CREATE TABLE public.flashcard_progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    set_id TEXT NOT NULL CHECK (length(set_id) > 0),
    set_title TEXT CHECK (length(set_title) > 0),
    card_data JSONB NOT NULL DEFAULT '{}'::jsonb,
    stats JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT flashcard_progress_user_set_unique UNIQUE(user_id, set_id)
);

-- Drop existing sessions table to recreate with proper constraints
DROP TABLE IF EXISTS public.user_sessions CASCADE;

-- Create user_sessions table for session management
CREATE TABLE public.user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    session_id TEXT NOT NULL CHECK (length(session_id) > 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_activity TIMESTAMPTZ NOT NULL DEFAULT now(),
    user_agent TEXT,
    ip_address INET,
    is_active BOOLEAN NOT NULL DEFAULT true,
    CONSTRAINT user_sessions_session_unique UNIQUE(session_id)
);

-- Enable RLS and create strict policies
ALTER TABLE public.flashcard_progress ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Users can view own progress" ON public.flashcard_progress;
DROP POLICY IF EXISTS "Users can insert own progress" ON public.flashcard_progress;
DROP POLICY IF EXISTS "Users can update own progress" ON public.flashcard_progress;
DROP POLICY IF EXISTS "Users can delete own progress" ON public.flashcard_progress;

-- Create strict RLS policies
CREATE POLICY "flashcard_select_policy" 
ON public.flashcard_progress 
FOR SELECT 
USING (auth.uid() IS NOT NULL AND auth.uid() = user_id);

CREATE POLICY "flashcard_insert_policy" 
ON public.flashcard_progress 
FOR INSERT 
WITH CHECK (auth.uid() IS NOT NULL AND auth.uid() = user_id);

CREATE POLICY "flashcard_update_policy" 
ON public.flashcard_progress 
FOR UPDATE 
USING (auth.uid() IS NOT NULL AND auth.uid() = user_id)
WITH CHECK (auth.uid() IS NOT NULL AND auth.uid() = user_id);

CREATE POLICY "flashcard_delete_policy" 
ON public.flashcard_progress 
FOR DELETE 
USING (auth.uid() IS NOT NULL AND auth.uid() = user_id);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS flashcard_progress_user_set_idx 
ON public.flashcard_progress (user_id, set_id);

-- Enable RLS for sessions table
ALTER TABLE public.user_sessions ENABLE ROW LEVEL SECURITY;

-- Drop existing session policies if they exist
DROP POLICY IF EXISTS "Users can view own sessions" ON public.user_sessions;
DROP POLICY IF EXISTS "Users can insert own sessions" ON public.user_sessions;
DROP POLICY IF EXISTS "Users can update own sessions" ON public.user_sessions;
DROP POLICY IF EXISTS "Users can delete own sessions" ON public.user_sessions;

-- Create strict session policies
CREATE POLICY "session_select_policy" 
ON public.user_sessions 
FOR SELECT 
USING (auth.uid() IS NOT NULL AND auth.uid() = user_id);

CREATE POLICY "session_insert_policy" 
ON public.user_sessions 
FOR INSERT 
WITH CHECK (auth.uid() IS NOT NULL AND auth.uid() = user_id);

CREATE POLICY "session_update_policy" 
ON public.user_sessions 
FOR UPDATE 
USING (auth.uid() IS NOT NULL AND auth.uid() = user_id)
WITH CHECK (auth.uid() IS NOT NULL AND auth.uid() = user_id);

CREATE POLICY "session_delete_policy" 
ON public.user_sessions 
FOR DELETE 
USING (auth.uid() IS NOT NULL AND auth.uid() = user_id);

-- Create index for session queries
CREATE INDEX IF NOT EXISTS user_sessions_user_id_idx 
ON public.user_sessions (user_id);

CREATE INDEX IF NOT EXISTS user_sessions_session_id_idx 
ON public.user_sessions (session_id);

