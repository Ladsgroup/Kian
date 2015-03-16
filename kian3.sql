SELECT page_title, cl_to FROM categorylinks
LEFT JOIN page_props ON cl_from=pp_page AND pp_propname="wikibase_item"
JOIN page on cl_from= page_id
WHERE page_namespace=0
AND page_is_redirect=0
AND pp_propname IS NULL;
