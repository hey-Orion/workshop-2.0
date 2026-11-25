Where does Pydantic sit in Dataflow Sentinel, and what does it catch that a dbt test wouldn't?

so pydantic sits in the first layer as a data gate keeper so that bad records filter out in the start so that the bad records never reach the analatics layer it catachse the wrong data types upper characters length of the tikcers and records in my project dbt comes in the most last part wit hbigquery after the data has been filterd
and calculated i do further calculations and vesulitions with dbt and bigquery.


Name three v1 → v2 renames (such as .dict(), @validator, and parse_obj).

in pydantic v2 they chaged the function names so it wont colide with the user defined fields 

first change .dict() to .model_dump()
and .json() to .model_dump_json()

second .parse_obj() to .model_vaildate()

third .validator to .field_validator()
to validate individual fields with @classmethod 
