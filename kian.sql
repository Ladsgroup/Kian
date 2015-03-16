select pp_value, cl_to from page_props join categorylinks on pp_page = cl_from join page on cl_from = page_id where pp_propname = 'wikibase_item' and page_namespace=0 AND page_is_redirect=0;
