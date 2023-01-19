create table Ad_provider
(
    id              int unsigned auto_increment
        primary key,
    company_name    varchar(128)                         not null,
    contact_email   varchar(128)                         not null,
    date_registered datetime default current_timestamp() not null
);

create table Campaign_payments
(
    id              int unsigned auto_increment
        primary key,
    payment_date    datetime default current_timestamp() not null,
    billing_address varchar(256)                         null,
    amount          decimal                              not null,
    tax             decimal                              not null,
    fee             decimal                              not null,
    provider_id     int unsigned                         not null,
    constraint Campaign_payments_Ad_provider_id_fk
        foreign key (provider_id) references Ad_provider (id)
);

create table Campaign
(
    id                    int unsigned auto_increment
        primary key,
    start_date            datetime     not null comment 'Can infer if is active by looking at the dates',
    end_date              datetime     not null,
    requester_ad_provider int unsigned not null,
    payment_id            int unsigned null,
    remaining_funds       decimal      not null comment 'Remaining funds used to payout clicks on an ad',
    payout_per_view       decimal      not null,
    constraint Campaign_Ad_provider_id_fk
        foreign key (requester_ad_provider) references Ad_provider (id),
    constraint Campaign_Campaign_payments_id_fk
        foreign key (payment_id) references Campaign_payments (id)
);

create table Category_tags
(
    id          int unsigned auto_increment
        primary key,
    name        varchar(256)  not null,
    description varchar(1024) null
);

create table `Space&Ad_type`
(
    id   int unsigned auto_increment
        primary key,
    type varchar(128) not null
)
    comment 'Describes type of resource';

create table Ads
(
    id             int unsigned auto_increment
        primary key,
    name           varchar(128)                         not null,
    provider_id    int unsigned                         not null,
    type           int unsigned                         not null,
    content_route  varchar(256)                         not null comment 'URL to the ad''s content',
    redirect_url   varchar(128)                         not null,
    date_submitted datetime default current_timestamp() not null,
    constraint Ads_Ad_provider_id_fk
        foreign key (provider_id) references Ad_provider (id),
    constraint Ads___fk_Type
        foreign key (type) references `Space&Ad_type` (id)
);

create table Ad_categories
(
    id              int unsigned auto_increment
        primary key,
    ad_id           int unsigned not null,
    category_tag    int unsigned not null,
    relative_weight int          not null comment 'Tag importance',
    constraint Ad_categories_Ads_id_fk
        foreign key (ad_id) references Ads (id),
    constraint Ad_categories___fk
        foreign key (category_tag) references Category_tags (id)
);

create table Campaign_ads
(
    id          int unsigned auto_increment
        primary key,
    campaign_id int unsigned not null,
    ad_id       int unsigned not null,
    constraint Campaign_ads_Ads_id_fk
        foreign key (ad_id) references Ads (id),
    constraint Campaign_ads_Campaign_id_fk
        foreign key (campaign_id) references Campaign (id)
)
    comment 'All ads to be listed in a campaign';

create table Space_provider
(
    id                   int unsigned auto_increment
        primary key,
    company_name         varchar(128)                         not null,
    contact_email        varchar(128)                         not null,
    date_registered      datetime default current_timestamp() not null,
    payment_interval     int                                  not null comment 'In days',
    last_payment         datetime                             null,
    payment_account_iban char(39)                             not null,
    constraint Space_provider_pk
        unique (company_name)
);

create table Space_payments
(
    id           int unsigned auto_increment
        primary key,
    payment_date datetime default current_timestamp() not null,
    amount       decimal                              not null,
    provider_id  int unsigned                         not null,
    tax          decimal                              not null,
    constraint Space_payments_Space_provider_id_fk
        foreign key (provider_id) references Space_provider (id)
);

create table Spaces
(
    id             int unsigned auto_increment
        primary key,
    name           varchar(128)                         not null,
    space_route    varchar(256)                         not null comment 'URL to the page which contains the space',
    provider_id    int unsigned                         not null,
    type           int unsigned                         not null,
    date_submitted datetime default current_timestamp() not null,
    funds_acquired decimal  default 0                   not null,
    constraint Spaces___fk
        foreign key (provider_id) references Space_provider (id),
    constraint Spaces___fk2_Type
        foreign key (type) references `Space&Ad_type` (id)
);

create table Campaign_spaces
(
    id              int unsigned auto_increment
        primary key,
    campaign_id     int unsigned not null,
    space_id        int unsigned not null,
    assigned_weight decimal      not null comment 'Used to determine bias for a cerain space to be chosen',
    constraint Campaign_spaces_Campaign_id_fk
        foreign key (campaign_id) references Campaign (id),
    constraint Campaign_spaces_Spaces_id_fk
        foreign key (space_id) references Spaces (id)
)
    comment 'Assigned automatically to a campaign based on the ad tags';

create table Hits
(
    id                int unsigned auto_increment
        primary key,
    viewer_ip         char(15)                             not null comment 'Used to identify geolocation',
    clicked           tinyint(1)                           not null comment 'Boolean value',
    campaign_space_id int unsigned                         not null,
    campaign_ad_id    int unsigned                         not null,
    date              datetime default current_timestamp() not null,
    hit_payout        decimal                              not null,
    constraint Hits_Campaign_ads_id_fk
        foreign key (campaign_ad_id) references Campaign_ads (id),
    constraint Hits_Campaign_spaces_id_fk
        foreign key (campaign_space_id) references Campaign_spaces (id)
)
    comment 'Identify view of an ad in a campaign';

create table Space_categories
(
    id              int unsigned auto_increment
        primary key,
    space_id        int unsigned not null,
    category_tag    int unsigned null,
    relative_weight int          not null comment 'Tag importance',
    constraint Space_categories___fk_space_id
        foreign key (space_id) references Spaces (id),
    constraint Space_categories___fk_tag
        foreign key (category_tag) references Category_tags (id)
);

