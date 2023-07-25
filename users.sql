create table if not exists test_flask.users
(
    id         int auto_increment
        primary key,
    email      varchar(150)                        not null,
    first_name varchar(150)                        not null,
    last_name  varchar(150)                        null,
    avatar     varchar(255)                        null,
    created_at timestamp default CURRENT_TIMESTAMP not null,
    updated_at timestamp default CURRENT_TIMESTAMP null,
    deleted_at timestamp                           null
);

create index users_created_at_index
    on test_flask.users (created_at desc);
