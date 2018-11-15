--Question 1:
-- Year is 2013 and all departure airports are based out of NYC

SELECT count(*) 
FROM rodriglr."table_flights.csv" 
WHERE dest = 'SEA'

-- Ans: 3885

--Question 2:

SELECT count(DISTINCT carrier) 
FROM rodriglr."table_flights.csv" 
WHERE dest = 'SEA'

-- Ans: 5

--Question 3:

SELECT count(DISTINCT tailnum) AS 'No. of unique airlines'
FROM rodriglr."table_flights.csv" 
WHERE dest = 'SEA'

--Ans: 933

--Question 4:

SELECT AVG(arr_delay) AS "Average_arrival_delay"
FROM rodriglr."flights.csv"
WHERE dest='SEA'

--Ans: -1.0990990990990991

--Question 5: 

SELECT (count(dest)*1.0/
        (SELECT COUNT(*)
         FROM rodriglr."flights.csv"
         WHERE dest = 'SEA')) as Percentage_of_flights, origin 
FROM rodriglr."flights.csv" 
WHERE dest = 'SEA'
GROUP BY origin

--Ans: Screenshot

--Question 6:

SELECT year, month, day, AVG (arr_delay) AS "average_arrival_delay"
FROM rodriglr."flights.csv"
GROUP BY year,month,day
ORDER BY Average_arrival_delay DESC
LIMIT 1;

SELECT year, month, day, AVG (dep_delay) AS "average_departure_delay"
FROM rodriglr."flights.csv"
GROUP BY year,month,day
ORDER BY Average_departure_delay DESC
LIMIT 1
--Question 7:

SELECT year,  month, day ,( AVG (dep_delay)* 1.0 / (COUNT(flight))) as delay_per_flight
FROM rodriglr."flights.csv"
WHERE dep_delay >0
GROUP BY year,month,day
ORDER BY ratio DESC
LIMIT 1


--Question 8:

SELECT AVG (dep_delay) AS "Avg. Autumn Monthly Dep Delay"
    FROM rodriglr."flights.csv"
    WHERE month IN (9,10,11)

SELECT AVG (dep_delay) AS "Avg. Monthly Dep Delay"
    FROM rodriglr."flights.csv"
    WHERE month IN (6,7,8)

--SELECT AVG ("Avg. Monthly Dep Delay") AS "Average Summer Dep Delay" 
--FROM 
  --  (SELECT month, AVG (dep_delay) AS "Avg. Monthly Dep Delay"
    --FROM rodriglr."flights.csv"
    --WHERE month IN (6,7,8)
    --GROUP BY month) as temp

--Question 9:

SELECT AVG (dep_delay) AS "Average_Hourly_Delay", (CASE WHEN hour = 24 THEN 0 ELSE hour END) as av_hour
    FROM rodriglr."flights.csv"
    GROUP BY av_hour

--Question 10:

SELECT year, month, day, flight, tailnum, (distance* 60.0/air_time) as mph_speed
    FROM rodriglr."flights.csv"
    ORDER BY mph_speed DESC
    LIMIT 1


--Question 11:

SELECT carrier, flight,dest , COUNT(DISTINCT (CONCAT (day, '-', month, '-', year))) AS newdate 
FROM rodriglr."table_flights.csv"
GROUP BY carrier,flight,dest
ORDER BY newdate DESC
LIMIT 1

--Question 12:
/*
I define delayed as anything more than 60 minutes delay and on time as anything with delay between -15 and 0. 
*/

SELECT ROUND(AVG(dep_delay),2) as avg_delay,
ROUND(AVG(visib),2) as avg_visib,
ROUND(AVG(temp),2) as avg_temp,
flight, tailnum
FROM rodriglr."flights.csv" f
INNER JOIN rodriglr."weather.csv" w
ON f.year = w.year AND
f.month = w.month AND
f.day = w.day AND
f.hour = w.hour
WHERE dep_delay > 60
group by flight,tailnum
ORDER by avg_delay ASC


SELECT ROUND(AVG(dep_delay),2) as avg_delay,
ROUND(AVG(visib),2) as avg_visib,
ROUND(AVG(temp),2) as avg_temp,
f.month, f.day
FROM rodriglr."flights.csv" f
INNER JOIN rodriglr."weather.csv" w
ON f.year = w.year AND
f.month = w.month AND
f.day = w.day AND
f.hour = w.hour
WHERE dep_delay BETWEEN -15 and 0
group by f.month, f.day
ORDER by avg_delay DESC


--Question 13:

/*

For flights from New York to Seattle, which airlines have the best performance in terms of delays

This question is interesting because it helps people who do not like flight delays and who want the best flight in terms of the least
arrival and departure delay.

As you can see from the above plots, AS (Alaska Airlines) has the least average departure delay and the least
average arrival delay as well while United Airlines (UA) has the highest average departure delay for flights to
Seattle. B6 has the highest average arrival delay for flights from NYC to Seattle. Hence, people who want departures & 
arrivals on time should choose Alaska Airlines. This inference  
have one problem which we did not consider is that since Alaska Airlines is based out of Seattle, hence might
have more flights in this route which might have resulted in the lower departure delay. But as we can see
from the below table, that is not the case. Hence we can safely say that Alaska Airlines has a good track
record of arriving and departing on time.
*/

SELECT ROUND(AVG(dep_delay),2) as avg_dep_delay,
ROUND(AVG(arr_delay),2) as avg_arr_delay,
carrier
FROM rodriglr."flights.csv" f
WHERE dest='SEA'
group by carrier
ORDER by avg_arr_delay, avg_dep_delay DESC

SELECT COUNT(tailnum),
carrier
FROM rodriglr."flights.csv" f
WHERE dest='SEA'
group by carrier
ORDER by COUNT(tailnum) ASC

SELECT ROUND(((AVG(dep_delay) + AVG(arr_delay))/2/COUNT(tailnum)),7)  as avg_total_delay_per_flight, 
ROUND(AVG(dep_delay),2) as average_dep_delay,
Round(AVG(arr_delay),2) as average_arr_delay,
COUNT(tailnum) as total_flights,
carrier
FROM rodriglr."flights.csv" f
WHERE dest='SEA'
group by carrier
ORDER by avg_total_delay_per_flight ASC