use mysql_async::prelude::*;

#[derive(Debug, PartialEq, Eq, Clone)]
struct TableColumn {
    field: Option<String>,
    type_: Option<String>,
    collation: Option<String>,
    null: Option<String>,
    key: Option<String>,
    default_: Option<String>,
    extra: Option<String>,
    privileges: Option<String>,
    comment: Option<String>
}

#[tokio::main]
async fn main() -> Result<(), mysql_async::error::Error> {
    /* ... */
    let database_url = "mysql://eridanus:eridanus@localhost:3308/eridanus";
    let pool = mysql_async::Pool::new(database_url);
    let mut conn = pool.get_conn().await?;
    let table_result = conn.query(r"show tables;").await?;
    let(_, tables) = table_result.map_and_drop(|row| {
        let table: Option<String> = mysql_async::from_row(row);
        table.unwrap()
    }).await?;
    for table in tables {
        conn = pool.get_conn().await?;
        let columns_result = conn.query("show full columns from ".to_string() + &table).await?;
        let (_ /* conn */, columns) = columns_result.map_and_drop(|row| {
            let (field, type_, collation, null, key, default, extra, privileges, comment) = mysql_async::from_row(row);
            TableColumn {
                field: field,
                type_: type_,
                collation: collation,
                null: null,
                key: key,
                default_: default,
                extra: extra,
                privileges: privileges,
                comment: comment
            }
        }).await?;
    }
    // The destructor of a connection will return it to the pool,
    // but pool should be disconnected explicitly because it's
    // an asynchronous procedure.
    pool.disconnect().await?;

    // the async fn returns Result, so
    Ok(())
}