  DROP SEQUENCE KIDS_NOTIFICATION_SQ;
  DROP SEQUENCE KIDS_ENCOUNTER_SQ;
  DROP SEQUENCE KIDS_LOCATION_SQ;
  DROP SEQUENCE AUTHENTICATION_ACCOUNT_SQ;
  DROP SEQUENCE KIDS_KID_SQ;
  
  /
  
  CREATE SEQUENCE KIDS_NOTIFICATION_SQ START WITH 1 INCREMENT BY 1;
  CREATE SEQUENCE KIDS_ENCOUNTER_SQ START WITH 1 INCREMENT BY 1;
  CREATE SEQUENCE KIDS_LOCATION_SQ START WITH 1 INCREMENT BY 1;
  CREATE SEQUENCE AUTHENTICATION_ACCOUNT_SQ START WITH 1 INCREMENT BY 1;
  CREATE SEQUENCE KIDS_KID_SQ START WITH 1 INCREMENT BY 1;
  
  /
  
  
  CREATE OR REPLACE TRIGGER "PROJECT_ADMIN"."KIDS_NOTIFICATION_TR" 
BEFORE INSERT ON "KIDS_NOTIFICATION"
FOR EACH ROW
 WHEN (new."ID" IS NULL) BEGIN
        SELECT "KIDS_NOTIFICATION_SQ".nextval
        INTO :new."ID" FROM dual;
    END;

/
ALTER TRIGGER "PROJECT_ADMIN"."KIDS_NOTIFICATION_TR" ENABLE;

/

  CREATE OR REPLACE TRIGGER "PROJECT_ADMIN"."KIDS_ENCOUNTER_TR" 
BEFORE INSERT ON "KIDS_ENCOUNTER"
FOR EACH ROW
 WHEN (new."ID" IS NULL) BEGIN
        SELECT "KIDS_ENCOUNTER_SQ".nextval
        INTO :new."ID" FROM dual;
    END;

/
ALTER TRIGGER "PROJECT_ADMIN"."KIDS_ENCOUNTER_TR" ENABLE;

/

  CREATE OR REPLACE TRIGGER "PROJECT_ADMIN"."KIDS_LOCATION_TR" 
BEFORE INSERT ON "KIDS_LOCATION"
FOR EACH ROW
 WHEN (new."ID" IS NULL) BEGIN
        SELECT "KIDS_LOCATION_SQ".nextval
        INTO :new."ID" FROM dual;
    END;
    
/

ALTER TRIGGER "PROJECT_ADMIN"."KIDS_LOCATION_TR" ENABLE;

/

CREATE OR REPLACE TRIGGER "PROJECT_ADMIN"."AUTHENTICATION_ACCOUNT_TR" 
BEFORE INSERT ON "AUTHENTICATION_ACCOUNT"
FOR EACH ROW
 WHEN (new."ID" IS NULL) BEGIN
        SELECT "AUTHENTICATION_ACCOUNT_SQ".nextval
        INTO :new."ID" FROM dual;
    END;
    
/

ALTER TRIGGER "PROJECT_ADMIN"."AUTHENTICATION_ACCOUNT_TR" ENABLE;

/

 CREATE OR REPLACE TRIGGER "PROJECT_ADMIN"."KIDS_KID_TR" 
BEFORE INSERT ON "KIDS_KID"
FOR EACH ROW
 WHEN (new."ID" IS NULL) BEGIN
        SELECT "KIDS_KID_SQ".nextval
        INTO :new."ID" FROM dual;
    END;

/

ALTER TRIGGER "PROJECT_ADMIN"."KIDS_KID_TR" ENABLE;

/

 CREATE OR REPLACE TRIGGER "PROJECT_ADMIN"."NOTIFICATIONS_ON_ENCOUNTER" 
AFTER INSERT ON "KIDS_ENCOUNTER"
FOR EACH ROW
declare
  name_1 varchar2(50);
  name_2 varchar2(50);
--  pragma autonomous_transaction;
begin
   select first_name||' '||last_name into name_1 from "PROJECT_ADMIN"."KIDS_KID" where id = :NEW.KID_1_ID;
   select first_name||' '||last_name into name_2 from "PROJECT_ADMIN"."KIDS_KID" where id = :NEW.KID_2_ID;
   
   INSERT INTO "PROJECT_ADMIN"."KIDS_NOTIFICATION" (id, notification_type, text, seen, date_created, kid_id) values 
        ("KIDS_NOTIFICATION_SQ".nextval, 'encounter', 'Has encountered '||name_2, 0, :NEW.DATE_CREATED, :NEW.KID_1_ID);
        
   INSERT INTO "PROJECT_ADMIN"."KIDS_NOTIFICATION" (id, notification_type, text, seen, date_created, kid_id) values 
        ("KIDS_NOTIFICATION_SQ".nextval, 'encounter', 'Has encountered '||name_1, 0, :NEW.DATE_CREATED, :NEW.KID_2_ID);
END;
/

ALTER TRIGGER "PROJECT_ADMIN"."NOTIFICATIONS_ON_ENCOUNTER" ENABLE;
/

CREATE OR REPLACE TRIGGER "PROJECT_ADMIN"."ENCOUNTER_ON_LOCATION"
AFTER INSERT ON "KIDS_LOCATION"
for each row
DECLARE
  pragma autonomous_transaction;
BEGIN
  children_functions.checkNeighbours(:NEW.kid_id, 10, :NEW.x, :NEW.y);
END;
/

ALTER TRIGGER "PROJECT_ADMIN"."ENCOUNTER_ON_LOCATION" ENABLE;
/