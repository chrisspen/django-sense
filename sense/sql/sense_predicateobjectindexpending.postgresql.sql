/*
2013.9.22 CKS
Finds all unique predicate+object pairs that need to be populated
into the predicate object index table.
*/
DROP VIEW IF EXISTS sense_predicateobjectindexpending CASCADE;
CREATE OR REPLACE VIEW sense_predicateobjectindexpending
AS
SELECT      CONCAT(CAST(sc_top.id AS VARCHAR), '-', CAST(st.predicate_id AS VARCHAR), '-', CAST(st.object_id AS VARCHAR)) AS id,
            sc_top.id AS context_id,
            st.predicate_id,
            st.object_id,
            COUNT(st.id) AS subject_count_direct
FROM        sense_triple AS st
INNER JOIN  sense_context_triples AS sct
        ON  sct.triple_id = st.id
        AND st.deleted IS NULL
        AND st.inferred = false
INNER JOIN  sense_context AS sc
        ON  sc.id = sct.context_id
INNER JOIN  sense_context AS sc_top
        ON  sc_top.id = sc.top_parent_id
INNER JOIN  sense_sense AS sp
        ON  sp.id = st.predicate_id
        AND sp.allow_predicate_usage = true
LEFT OUTER JOIN sense_predicateobjectindex AS spoi
        ON  spoi.context_id = sc_top.id
        AND spoi.predicate_id = st.predicate_id
        AND spoi.object_id = st.object_id
        AND (spoi.depth = 0 OR spoi.depth IS NULL)
WHERE       spoi.id IS NULL
        AND st.deleted IS NULL
GROUP BY    sc_top.id,
            st.predicate_id,
            st.object_id;
