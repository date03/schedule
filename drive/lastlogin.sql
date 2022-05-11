SELECT user_number, user_lname, user_fname, last_login
FROM 'user_login'
NATURAL INNER JOIN 'user'
ORDER BY last_login DESC
;