from database.DB_connect import DBConnect
from model.airport import Airport
from model.tratta import Tratta


class DAO():

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from airports a order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV1(idMapA):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as peso
                from flights f  
                group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID 
                order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID """

        cursor.execute(query)

        for row in cursor:
           # result.append((idMapA[row["ORIGIN_AIRPORT_ID"]],
            #               idMapA[row["DESTINATION_AIRPORT_ID"]],
             #              row["peso"]
              #             ))
            result.append(Tratta(idMapA[row["ORIGIN_AIRPORT_ID"]],
                                idMapA[row["DESTINATION_AIRPORT_ID"]],
                                row["peso"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV2(idMapA):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.ORIGIN_AIRPORT_ID, t1.DESTINATION_AIRPORT_ID, coalesce (t1.n,0) + coalesce(t2.n, 0) as peso
            from( select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as n
            from flights f 
            group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID 
            order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID ) t1
            left join (select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as n
            from flights f 
            group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID 
            order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID ) t2
            on t1.ORIGIN_AIRPORT_ID=t2.DESTINATION_AIRPORT_ID 
            and t1.DESTINATION_AIRPORT_ID=t2.ORIGIN_AIRPORT_ID
            where t1.origin_airport_id < t1.destination_airport_id  or t2.origin_airport_id is null
            """

        cursor.execute(query)

        for row in cursor:
            # result.append((idMapA[row["ORIGIN_AIRPORT_ID"]],
            #               idMapA[row["DESTINATION_AIRPORT_ID"]],
            #              row["peso"]
            #             ))
            result.append(Tratta(idMapA[row["ORIGIN_AIRPORT_ID"]],
                                 idMapA[row["DESTINATION_AIRPORT_ID"]],
                                 row["peso"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(n, idMapA):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT  t.ID , t.IATA_CODE, count(*) as N
                        FROM (select a.ID, a.IATA_CODE , f.AIRLINE_ID, count(*)
                        from airports a, flights f
                        where a.ID = f.ORIGIN_AIRPORT_ID  
                        or a.ID  = f.DESTINATION_AIRPORT_ID 
                        group by a.ID, a.IATA_CODE, f.AIRLINE_ID ) t
                        group by t.ID , t.IATA_CODE
                        having N >= %s
                        order by N asc"""

        cursor.execute(query, (n,))

        for row in cursor:
            result.append(idMapA[row["ID"]])

        cursor.close()
        conn.close()
        return result


