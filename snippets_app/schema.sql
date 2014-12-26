create table snippets (
keyword text primary key,
message text not null default ''
);

insert into snippets values ('insert', 'Add new rows to a table');

