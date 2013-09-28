/*
2013.9.22 CKS
Finds the number of objects a subject is linked to by the same predicate.
If there are more than one, indicates that predicate doesn not imply a mutually
exclusive subject.
*/
DROP VIEW IF EXISTS sense_exclusivesubjectpredicate CASCADE;
CREATE OR REPLACE VIEW sense_exclusivesubjectpredicate
AS
SELECT      CONCAT(CAST(ss.id AS VARCHAR), '-', CAST(sp.id AS VARCHAR)) AS id,
            ss.id AS subject_sense_id,
            ws.text AS subject_word_text,
            sp.id AS predicate_sense_id,
            wp.text AS predicate_word_text,
            COUNT(t.id) AS object_count
FROM        sense_triple AS t
INNER JOIN  sense_sense AS ss
        ON  ss.id = t.subject_id
INNER JOIN  sense_word AS ws
        ON  ws.id = ss.word_id
INNER JOIN  sense_sense AS sp
        ON  sp.id = t.predicate_id
INNER JOIN  sense_word AS wp
        ON  wp.id = sp.word_id
GROUP BY    ss.id,
            ws.text,
            sp.id,
            wp.text
HAVING COUNT(t.id) > 1
ORDER BY COUNT(t.id) DESC;
--select * from sense_exclusivesubjectpredicate where predicate_sense_id=1