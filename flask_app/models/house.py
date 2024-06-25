from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE



class House:
    def __init__(self,data):
        self.id=data['id']
        self.user_id=data['user_id']
        self.type=data['type']
        self.house_type=data['house_type']
        self.mortage_validation=data['mortage_validation']
        self.admin_validation=data['admin_validation']
        self.mortage_monthly=data['mortage_monthly']
        self.location=data['location']
        self.price=data['price']
        self.bathroom=data['bathroom']
        self.beds=data['beds']
        self.surface=data['surface']
        self.description=data['description']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.owner=''
        self.owner_phone_number=''
        self.owner_email=''
        self.pic=''  
        
    @classmethod
    def create_a_house(cls,data):
        query="""INSERT INTO houses 
        (user_id,type,mortage_validation,mortage_monthly,location,price,bathroom,beds,surface,house_type,description)
        VALUES
        (%(user_id)s,%(type)s,%(mortage_validation)s,%(mortage_monthly)s,%(location)s,%(price)s,%(bathroom)s,%(beds)s,%(surface)s,%(house_type)s,%(description)s);"""
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def put_photos_for_the_house(cls,data):
        query="INSERT INTO pics (house_id,path) VALUES (%(house_id)s,%(path)s);"
        return connectToMySQL(DATABASE).query_db(query,data)
    


    @classmethod
    def select_one_house_with_owner(cls,data):
        query="""SELECT houses.*,users.id AS receiver_id,first_name,last_name,email,phone_number FROM houses JOIN users ON
            houses.user_id=users.id WHERE houses.id=%(id)s;"""
        result=connectToMySQL(DATABASE).query_db(query,data)
        return result[0]
    def get_one_house_all_pics(cls,data):
        query="SELECT path FROM pics WHERE house_id=%(house_id)s"
        result=connectToMySQL(DATABASE).query_db(query,data)
        pics=[]
        for pic in result:
            pics.append(pic)
        return pics

    
    @classmethod
    def select_all_houses_with_pic(cls):
        query="""SELECT houses.*, MIN(pics.path) AS selected_path
                FROM houses
                JOIN pics ON houses.id = pics.house_id
                GROUP BY houses.id;"""
        results=connectToMySQL(DATABASE).query_db(query)
        houses=[]
        for house in results:
            row= cls(house)
            row.pic=house['selected_path']
            houses.append(row)
        return houses
    
    @classmethod
    def select_houses_with_crita(cls,data):
        query = """SELECT houses.*, MIN(pics.path) AS path
                FROM houses
                JOIN pics ON houses.id = pics.house_id
                WHERE"""
        criteria= {key: value for key, value in data.items() if value}
        conditions = []

        if 'min_price' in criteria:
            conditions.append(f"houses.price >= {criteria['min_price']}")

        if 'max_price' in criteria:
            conditions.append(f"houses.price <= {criteria['max_price']}")

        if 'min_surface' in criteria:
            conditions.append(f"houses.surface >= {criteria['min_surface']}")

        if 'max_surface' in criteria:
            conditions.append(f"houses.surface <= {criteria['max_surface']}")

        if 'min_beds' in criteria:
            conditions.append(f"houses.beds >= {criteria['min_beds']}")

        if 'max_beds' in criteria:
            conditions.append(f"houses.beds <= {criteria['max_beds']}")

        if 'min_bathroom' in criteria:
            conditions.append(f"houses.bathroom >= {criteria['min_bathroom']}")

        if 'max_bathroom' in criteria:
            conditions.append(f"houses.bathroom <= {criteria['max_bathroom']}")

        if 'type' in criteria:
            conditions.append(f"houses.type = '{criteria['type']}'")

        if 'house_type' in criteria:
            conditions.append(f"houses.house_type = '{criteria['house_type']}'")

        if 'location' in criteria:
            conditions.append(f"houses.location = '{criteria['location']}'")

        if 'mortage_validation' in criteria:
            conditions.append(f"houses.mortage_validation = {criteria['mortage_validation']}")
        
        if 'min_mortage_monthly' in criteria:
            conditions.append(f"houses.mortage_monthly >= {criteria['min_mortage_monthly']}")
        
        if 'max_mortage_monthly' in criteria:
            conditions.append(f"houses.mortage_monthly <= {criteria['max_mortage_monthly']}")

        if conditions:
            query += " "+" AND ".join(conditions) +"GROUP BY houses.id"

        results = connectToMySQL(DATABASE).query_db(query)
        print(results,"🎈🎈🎈🎈🎈🎈")
        houses = []
        for house in results:
            row = cls(house)
            row.pic = house['path']
            houses.append(row)

        return houses


    @classmethod
    def update_a_house(cls,data):
        query="""UPDATE houses
                    SET
                        houses.type =%(type)s,
                        houses.house_type =%(house_type)s
                        houses.mortage_validation = %(mortage_validation)s,
                        houses.mortage_monthly = %(mortage_monthly)s,
                        houses.location = %(location)s,
                        houses.price = %(price)s,
                        houses.bathroom = %(bathroom)s,
                        houses.beds = %(beds)s,
                        houses.surface = %(surface)s,
                        houses.description = %(description)s,
                    WHERE  houses.id=%(id)s;"""
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def update_pics_of_the_house(cls,data):
        query="UPDATE pics SET path=%(path)s WHERE house_id=%(house_id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def delete_the_house_with_its_pictures(cls,data):
        query="""DELETE FROM houses WHERE houses.id=%(id)s;"""
        query1 = """DELETE FROM pics WHERE pics.house_id=%(house_id)s;"""
        r1 = connectToMySQL(DATABASE).query_db(query1,data)
        return connectToMySQL(DATABASE).query_db(query,data)
    

    @classmethod
    def select_all_houses_for_sale_with_pic(cls):
        query="""SELECT houses.*, MIN(pics.path) AS selected_path
                        FROM houses
                        JOIN pics ON houses.id = pics.house_id
                        WHERE houses.type = 'sale'
                        GROUP BY houses.id;
                        """
        results=connectToMySQL(DATABASE).query_db(query)
        print(results)
        houses=[]
        for house in results:
            row= cls(house)
            row.pic=house['selected_path']
            houses.append(row)
        return houses
    

    @classmethod
    def select_all_houses_for_rent_with_pic(cls):
        query="""SELECT houses.*, MIN(pics.path) AS selected_path
                        FROM houses
                        JOIN pics ON houses.id = pics.house_id
                        WHERE houses.type = 'rent'
                        GROUP BY houses.id;
                        ;"""
        results=connectToMySQL(DATABASE).query_db(query)
        print(results)
        houses=[]
        for house in results:
            row= cls(house)
            row.pic=house['selected_path']
            houses.append(row)
        return houses
    

    @classmethod
    def select_all_houses_for_mortgage_with_pic(cls):
        query="""SELECT houses.*, MIN(pics.path) AS selected_path
                        FROM houses
                        JOIN pics ON houses.id = pics.house_id
                        WHERE houses.mortage_validation = 1
                        GROUP BY houses.id;
                        ;"""
        results=connectToMySQL(DATABASE).query_db(query)
        print(results)
        houses=[]
        for house in results:
            row= cls(house)
            row.pic=house['selected_path']
            houses.append(row)
        return houses
    

    @classmethod
    def get_all_photos_for_one_house(cls,data):
        query="""SELECT houses.id AS house_id, pics.id AS pic_id, path
FROM houses
JOIN pics ON houses.id = pics.house_id WHERE pics.house_id=%(house_id)s"""
        results=connectToMySQL(DATABASE).query_db(query,data)
        pics=[]
        for pic in results:
            pics.append(pic)
            print(pics)
        return pics
    
    @classmethod
    def get_all_photos_for_one_house_id(cls,data):
        query='SELECT id ,path FROM pics WHERE house_id=%(house_id)s'
        results=connectToMySQL(DATABASE).query_db(query,data)
        pics=[]
        for pic in results:
            pics.append(pic)
            print(pics)
        return pics
    
    @classmethod 
    def delete_on_pic(cls,data):
        query= "DELETE FROM pics WHERE id =%(id)s"
        return connectToMySQL(DATABASE).query_db(query,data)
    

    @classmethod
    def admin_house_validate(cls):
        query="""SELECT houses.*, MIN(pics.path) AS selected_path
                        FROM houses
                        JOIN pics ON houses.id = pics.house_id
                        WHERE houses.admin_validation = 0 
                        GROUP BY houses.id;
                        ;"""
        results=connectToMySQL(DATABASE).query_db(query)
        print(results)
        houses=[]
        for house in results:
            row= cls(house)
            row.pic=house['selected_path']
            houses.append(row)
        return houses
    
    @classmethod
    def select_houses_with_pics_not_validate(cls):
        query="""select houses.*, MIN(path) as path FROM houses JOIN pics ON houses.id=pics.house_id WHERE houses.admin_validation=0 GROUP BY 
                        houses.id;"""
        result=connectToMySQL(DATABASE).query_db(query)
        pictures=[]
        for picture in result:
            row=cls(picture)
            row.pic=picture['path']
            pictures.append(row)
        return pictures

    @classmethod
    def get_my_houses(cls,data):
        query="""
                SELECT houses.*,MIN(path) AS path FROM houses JOIN pics ON houses.id=pics.house_id WHERE houses.user_id=%(user_id)s
                    GROUP BY houses.id """
        result=connectToMySQL(DATABASE).query_db(query,data)
        pictures=[]
        for picture in result:
            row=cls(picture)
            row.pic=picture['path']
            pictures.append(row)
        return pictures


