from database.DB_connect import DBConnect
from model.edge import Edge
from model.pilot import Pilot


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(a1,a2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct d.driverId, d.driverRef ,d.dob 
                    from races r ,results re, drivers d 
                    where r.raceId  = re.raceId and d.driverId =re.driverId and re.`position` is not null and r.`year` between %s and %s"""

        cursor.execute(query,(a1,a2))

        for row in cursor:
            results.append(Pilot(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(a1, a2,idMap):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.driverid as id1,t2.driverid as id2,count(*) as weight
                    from (select distinct d.driverId,re.constructorId,r.raceId 
                    from races r ,results re, drivers d 
                    where r.raceId  = re.raceId and d.driverId =re.driverId and re.`position` is not null and r.`year` between %s and %s) as t1,
                    (select distinct d.driverId, re.constructorId,r.raceId 
                    from races r ,results re, drivers d
                    where r.raceId  = re.raceId and d.driverId =re.driverId and re.`position` is not null and r.`year` between %s and %s) as t2
                    where t1.constructorid = t2.constructorid and t1.driverid !=t2.driverid and t1.driverid < t2.driverid  and t1.raceid=t2.raceid 
                    group by t1.driverId,t2.driverId"""

        cursor.execute(query, (a1, a2,a1,a2))

        for row in cursor:
            p1 = idMap[row["id1"]]
            p2 = idMap[row["id2"]]
            results.append(Edge(p1, p2, row["weight"]))

        cursor.close()
        conn.close()
        return results

