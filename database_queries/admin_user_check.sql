-- Check Django admin login users.
-- Django stores password as a hash, so the plain password cannot be viewed from SQL.
-- Login is valid only when the username exists, is active, and is_staff = true.

-- Check the specific admin username: useradmin
SELECT
    id,
    username,
    email,
    password AS password_hash,
    is_staff,
    is_superuser,
    is_active,
    last_login,
    date_joined
FROM auth_user
WHERE username = 'useradmin';

-- List all users allowed to access the custom admin dashboard.
SELECT
    id,
    username,
    email,
    is_staff,
    is_superuser,
    is_active,
    last_login,
    date_joined
FROM auth_user
WHERE is_staff = true
ORDER BY username;

