SELECT * FROM USER_language


CREATE OR REPLACE FUNCTION get_course_id_by_email(email VARCHAR(30))
RETURNS INTEGER AS 
$BODY$
  SELECT user_course.id
  FROM user_course
  JOIN user_student ON user_student.id = user_course.student_id
  WHERE user_student.email = email
$BODY$
LANGUAGE SQL;

SELECT * FROM get_course_id_by_email('halil@gmail.com')

CREATE TABLE payments
(
  id SERIAL PRIMARY KEY,
  Course_id INTEGER NOT NULL REFERENCES user_course(Id) ON DELETE CASCADE,
  Amount NUMERIC,
  Pay_date DATE NOT NULL
);

INSERT INTO payments(Course_id, Amount, Pay_date)
VALUES
(1, 15000, '2022-08-15'),
(2, 55000, '2022-08-05'),
(3, 5000, '2022-08-25');


CREATE OR REPLACE FUNCTION all_data()
RETURNS TABLE(course_name VARCHAR(30), start_date DATE, student VARCHAR(30), mentor VARCHAR(30), language VARCHAR(30))
AS 
$BODY$
  SELECT uc.name, uc.date_started, us.name, um.name, ul.name
  FROM user_course AS uc
  JOIN user_student AS us ON uc.student_id = us.id
  JOIN user_mentor AS um ON uc.mentor_id = um.id
  JOIN user_language AS ul ON uc.language_id = ul.id
$BODY$
LANGUAGE SQL;


SELECT * FROM all_data()


CREATE OR REPLACE FUNCTION all_income()
RETURNS TABLE(language  VARCHAR(30), sum_amount INTEGER)
AS 
$BODY$
  SELECT ul.name, SUM(pay.amount)
  FROM payments AS pay
  JOIN user_course AS uc ON pay.Course_id = uc.id
  JOIN user_language AS ul ON uc.language_id = ul.id
  GROUP BY ul.name
$BODY$
LANGUAGE SQL;


SELECT * FROM all_income()