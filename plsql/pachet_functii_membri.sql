
create or replace package children_functions as
  TYPE age_distribution IS VARRAY(20) of float;
  function getAge (child_id in kids_kid.id%type) return number;
  function getAgeDistribution(year in integer) return float;
  function getChildrenInThatMonth(month in integer) return number;
  function getDistance(x1 in float, y1 in float, x2 in float, y2 in float) return float;
  function getDistanceBetweenKids(p_x in float, p_y in float, p_kid_id in kids_kid.id%type) return float;
  procedure checkNeighbours(p_kid_id in kids_kid.id%type, distance in integer, p_x in float, p_y in float);
end children_functions;

/
create or replace package body children_functions as

function getAge
(child_id in kids_kid.id%type) 
return number as
    age number := 0; 
begin 
  select 
  floor((current_date - birth_date)/365.25)
  into age from kids_kid where id = child_id;
  
  return age;
end getAge; 



function getAgeDistribution
(year in integer)
return float is
    CURSOR children_cur IS
    SELECT *
    FROM kids_kid
    ORDER BY id ASC;
    
  distribution children_functions.age_distribution;
  current_age integer;
  total integer := 0;
  counter integer := 0;
begin
   FOR children_rec IN children_cur loop
     current_age := getAge(children_rec.id);
     if (current_age = year) then
        counter := counter + 1;
     end if;
     total := total + 1;
   end loop;
   
   return (counter / total) * 100;
end getAgeDistribution;

function getChildrenInThatMonth(month in integer)
 return number is
   counter integer := 0;   
 begin
    SELECT count(*) into counter
    FROM kids_kid
    Where month = extract(month from registered_date)
    and extract(year from registered_date) = extract(year from current_date)
    ORDER BY id ASC;
    
    return counter;
 end getChildrenInThatMonth;
 
 
 function getDistance(x1 in float, y1 in float, x2 in float, y2 in float)
 return float is
  v_return float;
  v_delta1 float;
  v_delta2 float;
  v_lat_sin float;
  v_lng_sin float;
  v_tmp float;
 begin
  v_delta1 := x2 - x1;
  v_delta2 := y2 - y1;
  v_lat_sin := sin(v_delta1 / 2.0);
  v_lng_sin := sin(v_delta2 / 2.0);
  v_tmp := power(v_lat_sin, 2) + cos(x1) * cos(x2) * power(v_lng_sin, 2);
  v_return := 2 * asin(sqrt(v_tmp));
  return v_return * 6371000;
 end getDistance;


function getDistanceBetweenKids(p_x in float, p_y in float, p_kid_id in kids_kid.id%type) 
return float is
 x2 float;
 y2 float;
 PRAGMA AUTONOMOUS_TRANSACTION;
begin
    select latitude, longitude into x2, y2 from
      (select latitude, longitude from kids_location where kid_id = p_kid_id order by date_created desc)
        where rownum = 1;
    
    return getDistance(p_x, p_y, x2, y2);
    
  EXCEPTION WHEN OTHERS THEN
   return -1;
end getDistanceBetweenKids;

procedure checkNeighbours(p_kid_id in kids_kid.id%type, distance in integer, p_x in float, p_y in float) is
  v_last_x1 float;
  v_last_y1 float;
  v_last_x2 float;
  v_last_y2 float;
  v_distance float;
--  PRAGMA AUTONOMOUS_TRANSACTION;
begin
  
  for i in (select id from kids_kid where id <> p_kid_id) loop
    v_distance := getDistanceBetweenKids(p_x, p_y, i.id);

    if (v_distance <= distance and v_distance >= 0) then
      begin  

            select latitude, longitude into v_last_x1, v_last_y1 from (Select latitude, longitude, rownum as rn from(Select * from kids_location k where k.kid_id = p_kid_id order by k.date_created desc))
            where rn=1;

            select latitude, longitude into v_last_x2, v_last_y2 from (Select latitude, longitude, rownum as rn from(Select * from kids_location k where k.kid_id = i.id order by k.date_created desc))
            where rn=2;    

            if ((getDistance(v_last_x1, v_last_y1, v_last_x2, v_last_y2) > distance))  then  

                insert into kids_encounter 
                  (date_created, kid_1_id, kid_2_id) 
                     values (sysdate, p_kid_id, i.id);
                commit;
                return;
            end if;

           EXCEPTION WHEN NO_DATA_FOUND THEN
           insert into kids_encounter 
              (date_created, kid_1_id, kid_2_id) 
                  values (sysdate, p_kid_id, i.id);
           commit;
           WHEN OTHERS THEN
           dbms_output.put_line(SUBSTR(SQLERRM, 1, 200));
      end;  
    end if;
  end loop;
  EXCEPTION WHEN OTHERS THEN
        NULL;
end checkNeighbours;
end children_functions;
/


set serveroutput on;
declare
  v_user_id authentication_account.id%type := 1; --189
  distribution children_functions.age_distribution;
begin
  dbms_output.put_line('The user '||v_user_id||' has: '||children_functions.getAge(v_user_id)||' years');
   for i in 0..10 loop
      dbms_output.put_line(i||' '||children_functions.getAgeDistribution(i)||'%');
   end loop;
    dbms_output.put_line(children_functions.getDistance(9, 7, 3, 2));
end;

/


set serveroutput on;
declare
  v_distance float;
  v_x1 float := 0.340978812473806;
  v_x2 float := -0.633783394530149;
  v_y1 float := -0.940070981066831;
  v_y2 float := -1.16331667485907;
begin
dbms_output.put_line(v_x1 + v_x2);
  v_distance := children_functions.getDistance(v_x1, v_y1, v_x2, v_y2);
  dbms_output.put_line(v_distance);
end;
  
/

                                                     
