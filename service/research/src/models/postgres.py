from models.datamodel import DataModelBookmark, DataModelLike, DataModelReview

tables = {
    DataModelLike:  {
        'sqls': 'SELECT * FROM table_like WHERE id = ',
        'sqli': """INSERT INTO table_like (
            like_value, author, film)
            VALUES """,
        'sqlm': '(%s,%s,%s)  RETURNING id;',
        'data': ('like_value', 'author', 'film',),
        'sqlc': """CREATE TABLE content.table_like
            (
                id serial primary key,
                like_value SMALLINT NOT NULL,
                author TEXT NOT NULL,
                film TEXT NOT NULL
            );
            """
    },
    DataModelReview: {
        'sqls': 'SELECT * FROM table_review WHERE id = ',
        'sqli': """INSERT INTO table_review (
            text, published, author, film)
            VALUES """,
        'sqlm': '(%s,%s,%s,%s) RETURNING id;',
        'data': ('text', 'published', 'author', 'film',),
        'sqlc': """CREATE TABLE content.table_review
            (
                id serial primary key,
                text TEXT NOT NULL,
                published TEXT NOT NULL,
                author TEXT NOT NULL,
                film TEXT NOT NULL
            );
            """
    },
    DataModelBookmark: {
        'sqls': 'SELECT * FROM table_bookmark WHERE id = ',
        'sqli': """INSERT INTO table_bookmark (
            author, film)
            VALUES """,
        'sqlm': '(%s,%s) RETURNING id;',
        'data': ('author', 'film',),
        'sqlc': """CREATE TABLE content.table_bookmark
            (
                id serial primary key,
                author TEXT NOT NULL,
                film TEXT NOT NULL
            );
            """
    },
}
