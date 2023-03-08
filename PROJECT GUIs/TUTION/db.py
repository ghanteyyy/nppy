import uuid
import sqlite3
import datetime


class DB:
    def __init__(self, db_file):
        self.db_file = db_file
        self.StartConnection()

        self.CreateTable()

    def __del__(self):
        self.EndConnection()

    def StartConnection(self):
        self.conn = sqlite3.connect(self.db_file)
        self.conn.execute("PRAGMA foreign_keys = ON")

        self.cur = self.conn.cursor()

    def EndConnection(self):
        self.cur.close()
        self.conn.close()

    def CreateTable(self):
        with self.conn:
            query1 = '''
            CREATE TABLE IF NOT EXISTS Student (
                ID          TEXT        PRIMARY KEY,
                Name        TEXT        NOT NULL,
                Fee         INTEGER     NOT NULL,
                Joined      TEXT        NOT NULL,
                NextPay     TEXT        NOT NULL
            )'''

            query2 = '''
            CREATE TABLE IF NOT EXISTS PreviousPays (
                ID          TEXT     PRIMARY KEY,
                StudentID   TEXT     NOT NULL,
                Dates       TEXT,
                FOREIGN KEY(StudentID) REFERENCES Student(ID) ON DELETE CASCADE
            )'''

            query3 = '''
            CREATE TABLE IF NOT EXISTS LatePays (
                ID          TEXT     PRIMARY KEY,
                PrevID      TEXT     NOT NULL,
                Days        TEXT,
                FOREIGN KEY(PrevID) REFERENCES PreviousPays(ID) ON DELETE CASCADE
            )'''

            for query in [query1, query2, query3]:
                self.cur.execute(query)

    def AddNewStudent(self, values):
        with self.conn:
            StudentID = uuid.uuid4().hex
            values = (StudentID,) + values

            self.cur.execute('''INSERT INTO STUDENT (ID, Name, Fee, Joined, NextPay)
                                VALUES (?, ?, ?, ?, ?)''', values)

    def UpdatePreviousPay(self, student_id, prevPayDate):
        with self.conn:
            prev_id = uuid.uuid4().hex

            self.cur.execute('''INSERT INTO PreviousPays (ID, StudentID, Dates)
                                VALUES (:id, :stud_id, :date)''',
                                {'id': prev_id, 'stud_id': student_id, 'date': prevPayDate})

    def UpdateLateDates(self, student_id, date, days):
        with self.conn:
            PrevDetails = self.cur.execute('''SELECT ID, StudentID, Dates FROM PreviousPays
                                              WHERE StudentID=? AND Dates=?''', (student_id, date)).fetchall()

            late_id = uuid.uuid4().hex
            prev_id, student_id, _ = PrevDetails[0]

            self.cur.execute('''INSERT INTO LatePays (ID, PrevID, Days)
                                VALUES (:lateID, :PrevID, :Days)''',
                                {'lateID': late_id, 'PrevID': prev_id, 'Days': days})

    def UpdateNextPay(self, student_id, nextPay):
        with self.conn:
            self.cur.execute('''UPDATE Student SET NextPay=:nextPay
                                WHERE ID=:stud_id''',
                                {'nextPay': nextPay, 'stud_id': student_id})

    def DeleteUser(self, id):
        with self.conn:
            self.cur.execute('''DELETE FROM Student WHERE ID=?''', (id,))

    def GetLeftAndLateDays(self, NextPayDate):
        today = datetime.date.today()
        next_pay_obj = datetime.datetime.strptime(NextPayDate, '%Y-%b-%d').date()

        left = (next_pay_obj - today).days

        if left < 0:
            return 0, abs(left)

        return left, 0

    def RetrieveData(self):
        contents = dict()
        BasicDetails = self.cur.execute('SELECT * FROM Student').fetchall()

        for BasicDetail in BasicDetails:
            id = BasicDetail[0]
            left, LatePay = self.GetLeftAndLateDays(BasicDetail[4])

            PreviousPayDetails = self.cur.execute('SELECT * FROM PreviousPays WHERE StudentID=?', (id,)).fetchall()

            if PreviousPayDetails:
                LastPrevDetails = PreviousPayDetails[-1]
                LastPayDate = LastPrevDetails[-1]

            else:
                LastPayDate = 'Not Yet'

            content = {
                id:
                    {
                        'Name': BasicDetail[1],
                        'Fee': BasicDetail[2],
                        'Joined': BasicDetail[3],
                        'PrevDate': LastPayDate,
                        'NextPay': BasicDetail[4],
                        'Left': left,
                        "LatePay": LatePay
                    }
            }

            contents.update(content)

        return contents
