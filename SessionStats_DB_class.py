import psycopg2
from dotenv import load_dotenv
import os
import datetime

load_dotenv() # load enviroment variables

class SessionStatsDB:

    def __init__(self):
        # connection info
        self.host ="localhost"
        self.database ="postgres"
        self.user = "postgres"
        self.password = os.getenv("POSTGRESS_PW")
    
    # insert individual battle stats into DB, single execution statement
    def insertBattle(self, battle_time, tank_id, tank_name, damage, wn8, kills, xp, win):

        query = f"""
        INSERT INTO session_stats(battle_time, tank_id, tank_name, damage, wn8, kills, xp, win)
        VALUES('{battle_time}', {tank_id}, '{tank_name}', {damage}, {wn8}, {kills}, {xp}, {win})
        RETURNING *;
        """
        try: 
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database to insert battle.')
            conn = psycopg2.connect(
                host = self.host,
                database = self.database,
                user = self.user,
                password = self.password)
            # create a cursor
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
            # close the communication with the PostgreSQL
            cur.close()
    
        except (Exception, psycopg2.DatabaseError) as error:
            print("-----------------------------------")
            print(error)
            print("-----------------------------------")
        finally:
            if conn is not None:
                conn.close()
                print('Database connection for insertBattle closed.')
    
    # returns best battle in the CURRENT SESSION (same as current date), ordered data in a tuple
    def bestBattle(self):
        
        query = f"""
        SELECT tank_name, damage, wn8, battle_time, kills, win
        FROM session_stats
        WHERE battle_date = CURRENT_DATE
        ORDER BY damage DESC;
        """
        try: 
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database to insert battle.')
            conn = psycopg2.connect(
                host = self.host,
                database = self.database,
                user = self.user,
                password = self.password)

            cur = conn.cursor()
            cur.execute(query)
            best_game = cur.fetchone()
            cur.close()
    
        except (Exception, psycopg2.DatabaseError) as error:
            print("-----------------------------------")
            print(error)
            print("-----------------------------------")
        finally:
            if conn is not None:
                conn.close()
                print('Database connection for insertBattle closed.')
            return best_game

#test = SessionStatsDB()
#print(test.bestBattle())