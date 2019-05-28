-- FUNCTION: public."GetFeatureCompareResult"(text, text)

-- DROP FUNCTION public."GetFeatureCompareResult"(text, text);

CREATE OR REPLACE FUNCTION public."GetFeatureCompareResult"(
	target_table_name text DEFAULT 'image_target'::text,
	source_table_name text DEFAULT 'image50w'::text)
    RETURNS void
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
AS $BODY$declare i float[];
	j float[][];
	h float[];
	mysql1 text;
	mysql2 text; 
begin
 mysql1 := 'select feature::float[] from '
		|| quote_ident(target_table_name);
for i in execute mysql1
loop
execute 'select feature::float[] from '
	|| quote_ident(source_table_name)
	|| ' order by cube(feature) <-> cube($1)' using i into h;
raise notice '%', h; 
end loop;

end;$BODY$;

ALTER FUNCTION public."GetFeatureCompareResult"(text, text)
    OWNER TO postgres;
