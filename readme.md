CREATE OR REPLACE FUNCTION notify_data_change() RETURNS trigger AS $$
BEGIN
    PERFORM pg_notify('table_update', 'Data changed in table ' || TG_TABLE_NAME);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER data_change_trigger
AFTER INSERT OR UPDATE OR DELETE ON scrapper_song
FOR EACH ROW EXECUTE FUNCTION notify_data_change();
