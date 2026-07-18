--
-- PostgreSQL database dump
--

\restrict gVKRd2hQvfGCarl0ptatB9h4wMIkE2op7DVKt02A6RIKTAYR1PTF7Q4eyLsTbaV

-- Dumped from database version 18.4 (Ubuntu 18.4-1.pgdg22.04+1)
-- Dumped by pg_dump version 18.4 (Ubuntu 18.4-1.pgdg22.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: action; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.action (
    action_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    action_name text NOT NULL,
    short_name text NOT NULL,
    sport_id uuid NOT NULL
);


ALTER TABLE public.action OWNER TO postgres;

--
-- Name: auth_actions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_actions (
    auth_action_id uuid NOT NULL,
    auth_action_name text NOT NULL
);


ALTER TABLE public.auth_actions OWNER TO postgres;

--
-- Name: blog; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.blog (
    blog_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    title text NOT NULL,
    author text NOT NULL,
    slug text NOT NULL,
    content text NOT NULL
);


ALTER TABLE public.blog OWNER TO postgres;

--
-- Name: blog_person; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.blog_person (
    blog_id uuid CONSTRAINT blog_personnel_blog_id_not_null NOT NULL,
    person_id uuid CONSTRAINT blog_personnel_person_id_not_null NOT NULL
);


ALTER TABLE public.blog_person OWNER TO postgres;

--
-- Name: blog_team; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.blog_team (
    blog_id uuid NOT NULL,
    team_id uuid NOT NULL
);


ALTER TABLE public.blog_team OWNER TO postgres;

--
-- Name: blog_tournament; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.blog_tournament (
    blog_id uuid NOT NULL,
    tournament_id uuid NOT NULL
);


ALTER TABLE public.blog_tournament OWNER TO postgres;

--
-- Name: country; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.country (
    country_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    country_name text NOT NULL
);


ALTER TABLE public.country OWNER TO postgres;

--
-- Name: game; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.game (
    game_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    game_venue text NOT NULL,
    game_date date NOT NULL,
    tournament_id uuid NOT NULL,
    home_team uuid NOT NULL,
    away_team uuid NOT NULL,
    match_source text
);


ALTER TABLE public.game OWNER TO postgres;

--
-- Name: game_actions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.game_actions (
    game_id uuid NOT NULL,
    team_id uuid NOT NULL,
    person_id uuid NOT NULL,
    action_id uuid NOT NULL,
    shot_clock time without time zone NOT NULL,
    action_timestamp timestamp without time zone,
    outcome text,
    period text,
    timer text,
    x1 double precision,
    y1 double precision,
    x2 double precision,
    y2 double precision,
    CONSTRAINT game_actions_period_check CHECK ((period = ANY (ARRAY['H1'::text, 'H2'::text, 'AET1'::text, 'AET2'::text, 'Q1'::text, 'Q2'::text, 'Q3'::text, 'Q4'::text, 'OT1'::text, 'OT2'::text]))),
    CONSTRAINT game_actions_timer_check CHECK ((timer = ANY (ARRAY['on'::text, 'off'::text])))
);


ALTER TABLE public.game_actions OWNER TO postgres;

--
-- Name: lineup; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lineup (
    game_id uuid NOT NULL,
    team_id uuid NOT NULL,
    person_id uuid NOT NULL,
    role text NOT NULL,
    is_captain boolean DEFAULT false,
    CONSTRAINT lineup_role_check CHECK ((role = ANY (ARRAY['Starter'::text, 'Substitute'::text, 'Unused_Substitute'::text])))
);


ALTER TABLE public.lineup OWNER TO postgres;

--
-- Name: organization; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.organization (
    organization_id uuid NOT NULL,
    organization_name text NOT NULL,
    organization_type text,
    CONSTRAINT organization_organization_type_check CHECK ((organization_type = ANY (ARRAY['SKWOD'::text, 'FEDERATION'::text, 'TEAM'::text, 'MEDIA'::text, 'BOOKMAKER'::text, 'DATA_PROVIDER'::text])))
);


ALTER TABLE public.organization OWNER TO postgres;

--
-- Name: permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.permissions (
    permission_id uuid NOT NULL,
    auth_action_id uuid,
    resource_id uuid
);


ALTER TABLE public.permissions OWNER TO postgres;

--
-- Name: person; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.person (
    person_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    person_name text NOT NULL,
    person_dob date,
    person_pic text,
    person_height double precision,
    person_weight double precision
);


ALTER TABLE public.person OWNER TO postgres;

--
-- Name: person_nationality; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.person_nationality (
    person_id uuid NOT NULL,
    country_id uuid NOT NULL
);


ALTER TABLE public.person_nationality OWNER TO postgres;

--
-- Name: person_participation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.person_participation (
    pp_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    pt_id uuid NOT NULL,
    tt_id uuid NOT NULL,
    pp_pic text
);


ALTER TABLE public.person_participation OWNER TO postgres;

--
-- Name: person_team; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.person_team (
    pt_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    team_id uuid NOT NULL,
    person_id uuid NOT NULL,
    person_type text NOT NULL,
    start_date date,
    end_date date,
    transfer_reason text,
    status text,
    pt_pic text,
    CONSTRAINT person_team_person_type_check CHECK ((person_type = ANY (ARRAY['Coach'::text, 'Player'::text]))),
    CONSTRAINT person_team_status_check CHECK ((status = ANY (ARRAY['ACTIVE'::text, 'INACTIVE'::text])))
);


ALTER TABLE public.person_team OWNER TO postgres;

--
-- Name: resources; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.resources (
    resource_id uuid NOT NULL,
    resource_name text NOT NULL
);


ALTER TABLE public.resources OWNER TO postgres;

--
-- Name: role_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.role_permissions (
    role_permission_id uuid NOT NULL,
    role_id uuid,
    permission_id uuid
);


ALTER TABLE public.role_permissions OWNER TO postgres;

--
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    role_id uuid NOT NULL,
    role_name text NOT NULL
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- Name: sport; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sport (
    sport_id uuid DEFAULT public.uuid_generate_v4() CONSTRAINT sports_id_not_null NOT NULL,
    sport_name text CONSTRAINT sports_name_not_null NOT NULL
);


ALTER TABLE public.sport OWNER TO postgres;

--
-- Name: team; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.team (
    team_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    team_name text NOT NULL,
    team_type text NOT NULL,
    nickname text,
    team_logo text,
    sport_id uuid NOT NULL,
    country_id uuid NOT NULL,
    CONSTRAINT team_team_type_check CHECK ((team_type = ANY (ARRAY['NT'::text, 'CLUB'::text])))
);


ALTER TABLE public.team OWNER TO postgres;

--
-- Name: team_tournament; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.team_tournament (
    tt_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    team_id uuid NOT NULL,
    tournament_id uuid NOT NULL
);


ALTER TABLE public.team_tournament OWNER TO postgres;

--
-- Name: tournament; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tournament (
    tournament_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    tournament_name text NOT NULL,
    season text,
    subcategory text,
    parent_tournament_id uuid,
    sport_id uuid NOT NULL
);


ALTER TABLE public.tournament OWNER TO postgres;

--
-- Name: user_roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_roles (
    user_role_id uuid NOT NULL,
    user_id uuid,
    role_id uuid,
    organization_id uuid
);


ALTER TABLE public.user_roles OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id uuid NOT NULL,
    organization_id uuid,
    user_email text NOT NULL,
    user_password_hash text NOT NULL,
    user_first_name text,
    user_last_name text,
    user_status text,
    CONSTRAINT users_user_status_check CHECK ((user_status = ANY (ARRAY['active'::text, 'inactive'::text])))
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Data for Name: action; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.action (action_id, action_name, short_name, sport_id) FROM stdin;
b5d454d5-18d3-4e36-bb3b-4bd57cce3dc3	Lacrosse Kick Off	LKO	1792b56e-3d90-4bf2-94e1-e4f5d5a88d35
\.


--
-- Data for Name: auth_actions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_actions (auth_action_id, auth_action_name) FROM stdin;
\.


--
-- Data for Name: blog; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.blog (blog_id, title, author, slug, content) FROM stdin;
7815f0a8-f152-439a-8f8d-a974873bac97	blog1	otivo	this is a test	In my FastApI project, this constitutes as my first blog test
\.


--
-- Data for Name: blog_person; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.blog_person (blog_id, person_id) FROM stdin;
7815f0a8-f152-439a-8f8d-a974873bac97	9e5cea95-2e10-420d-b3c5-e3d7203c3c18
\.


--
-- Data for Name: blog_team; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.blog_team (blog_id, team_id) FROM stdin;
7815f0a8-f152-439a-8f8d-a974873bac97	c48bbbaf-b808-4771-b3a6-767a7ee125f5
\.


--
-- Data for Name: blog_tournament; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.blog_tournament (blog_id, tournament_id) FROM stdin;
7815f0a8-f152-439a-8f8d-a974873bac97	4c59c887-c490-4d5a-b761-49b28cde453e
\.


--
-- Data for Name: country; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.country (country_id, country_name) FROM stdin;
0284fb49-d846-41ab-9d0f-50fcb2a6e9c2	Kenya
\.


--
-- Data for Name: game; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.game (game_id, game_venue, game_date, tournament_id, home_team, away_team, match_source) FROM stdin;
5c9c2b7e-343f-4412-bb86-7261e9ddd7ac	Ngong Stadium	2025-12-04	4c59c887-c490-4d5a-b761-49b28cde453e	c48bbbaf-b808-4771-b3a6-767a7ee125f5	a77f3564-8c71-471f-8c4e-44ae43c34431	\N
\.


--
-- Data for Name: game_actions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.game_actions (game_id, team_id, person_id, action_id, shot_clock, action_timestamp, outcome, period, timer, x1, y1, x2, y2) FROM stdin;
5c9c2b7e-343f-4412-bb86-7261e9ddd7ac	c48bbbaf-b808-4771-b3a6-767a7ee125f5	9e5cea95-2e10-420d-b3c5-e3d7203c3c18	b5d454d5-18d3-4e36-bb3b-4bd57cce3dc3	00:00:31	\N	\N	H1	on	50	50	0	0
\.


--
-- Data for Name: lineup; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.lineup (game_id, team_id, person_id, role, is_captain) FROM stdin;
5c9c2b7e-343f-4412-bb86-7261e9ddd7ac	c48bbbaf-b808-4771-b3a6-767a7ee125f5	9e5cea95-2e10-420d-b3c5-e3d7203c3c18	Starter	t
\.


--
-- Data for Name: organization; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.organization (organization_id, organization_name, organization_type) FROM stdin;
\.


--
-- Data for Name: permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.permissions (permission_id, auth_action_id, resource_id) FROM stdin;
\.


--
-- Data for Name: person; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.person (person_id, person_name, person_dob, person_pic, person_height, person_weight) FROM stdin;
9e5cea95-2e10-420d-b3c5-e3d7203c3c18	Otivo	1989-06-18	\N	\N	\N
\.


--
-- Data for Name: person_nationality; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.person_nationality (person_id, country_id) FROM stdin;
9e5cea95-2e10-420d-b3c5-e3d7203c3c18	0284fb49-d846-41ab-9d0f-50fcb2a6e9c2
\.


--
-- Data for Name: person_participation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.person_participation (pp_id, pt_id, tt_id, pp_pic) FROM stdin;
41561d02-c1ae-4ee9-89eb-dd7a2f9c08da	dfaccc74-d442-44ff-910a-9505fbf03362	0cb0e8b6-dd8d-4bad-9b5f-37a37d98d8df	\N
\.


--
-- Data for Name: person_team; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.person_team (pt_id, team_id, person_id, person_type, start_date, end_date, transfer_reason, status, pt_pic) FROM stdin;
dfaccc74-d442-44ff-910a-9505fbf03362	c48bbbaf-b808-4771-b3a6-767a7ee125f5	9e5cea95-2e10-420d-b3c5-e3d7203c3c18	Player	2025-12-01	2025-12-05	Contract Terminated	INACTIVE	\N
\.


--
-- Data for Name: resources; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.resources (resource_id, resource_name) FROM stdin;
\.


--
-- Data for Name: role_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.role_permissions (role_permission_id, role_id, permission_id) FROM stdin;
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles (role_id, role_name) FROM stdin;
\.


--
-- Data for Name: sport; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sport (sport_id, sport_name) FROM stdin;
1792b56e-3d90-4bf2-94e1-e4f5d5a88d35	Lacrosse
\.


--
-- Data for Name: team; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.team (team_id, team_name, team_type, nickname, team_logo, sport_id, country_id) FROM stdin;
c48bbbaf-b808-4771-b3a6-767a7ee125f5	111 FC	CLUB	\N	\N	1792b56e-3d90-4bf2-94e1-e4f5d5a88d35	0284fb49-d846-41ab-9d0f-50fcb2a6e9c2
a77f3564-8c71-471f-8c4e-44ae43c34431	Ngong FC	CLUB	Hills	\N	1792b56e-3d90-4bf2-94e1-e4f5d5a88d35	0284fb49-d846-41ab-9d0f-50fcb2a6e9c2
\.


--
-- Data for Name: team_tournament; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.team_tournament (tt_id, team_id, tournament_id) FROM stdin;
0cb0e8b6-dd8d-4bad-9b5f-37a37d98d8df	c48bbbaf-b808-4771-b3a6-767a7ee125f5	4c59c887-c490-4d5a-b761-49b28cde453e
\.


--
-- Data for Name: tournament; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tournament (tournament_id, tournament_name, season, subcategory, parent_tournament_id, sport_id) FROM stdin;
466398df-74a2-4542-8f85-77de767fe9eb	Road to BAL			\N	1792b56e-3d90-4bf2-94e1-e4f5d5a88d35
4c59c887-c490-4d5a-b761-49b28cde453e	Road to BAL	2026	Elite 16	466398df-74a2-4542-8f85-77de767fe9eb	1792b56e-3d90-4bf2-94e1-e4f5d5a88d35
\.


--
-- Data for Name: user_roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_roles (user_role_id, user_id, role_id, organization_id) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, organization_id, user_email, user_password_hash, user_first_name, user_last_name, user_status) FROM stdin;
\.


--
-- Name: action action_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.action
    ADD CONSTRAINT action_pkey PRIMARY KEY (action_id);


--
-- Name: auth_actions auth_actions_auth_action_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_actions
    ADD CONSTRAINT auth_actions_auth_action_name_key UNIQUE (auth_action_name);


--
-- Name: auth_actions auth_actions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_actions
    ADD CONSTRAINT auth_actions_pkey PRIMARY KEY (auth_action_id);


--
-- Name: blog_person blog_personnel_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.blog_person
    ADD CONSTRAINT blog_personnel_pkey PRIMARY KEY (blog_id, person_id);


--
-- Name: blog blog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.blog
    ADD CONSTRAINT blog_pkey PRIMARY KEY (blog_id);


--
-- Name: blog blog_slug_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.blog
    ADD CONSTRAINT blog_slug_key UNIQUE (slug);


--
-- Name: blog_team blog_team_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.blog_team
    ADD CONSTRAINT blog_team_pkey PRIMARY KEY (blog_id, team_id);


--
-- Name: blog_tournament blog_tournament_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.blog_tournament
    ADD CONSTRAINT blog_tournament_pkey PRIMARY KEY (blog_id, tournament_id);


--
-- Name: country country_country_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.country
    ADD CONSTRAINT country_country_name_key UNIQUE (country_name);


--
-- Name: country country_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.country
    ADD CONSTRAINT country_pkey PRIMARY KEY (country_id);


--
-- Name: game_actions game_actions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_actions
    ADD CONSTRAINT game_actions_pkey PRIMARY KEY (game_id, team_id, person_id, action_id, shot_clock);


--
-- Name: game game_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game
    ADD CONSTRAINT game_pkey PRIMARY KEY (game_id);


--
-- Name: lineup lineup_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lineup
    ADD CONSTRAINT lineup_pkey PRIMARY KEY (game_id, team_id, person_id);


--
-- Name: organization organization_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization
    ADD CONSTRAINT organization_pkey PRIMARY KEY (organization_id);


--
-- Name: permissions permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (permission_id);


--
-- Name: person_nationality person_nationality_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person_nationality
    ADD CONSTRAINT person_nationality_pkey PRIMARY KEY (person_id, country_id);


--
-- Name: person_participation person_participation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person_participation
    ADD CONSTRAINT person_participation_pkey PRIMARY KEY (pp_id);


--
-- Name: person person_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person
    ADD CONSTRAINT person_pkey PRIMARY KEY (person_id);


--
-- Name: person_team person_team_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person_team
    ADD CONSTRAINT person_team_pkey PRIMARY KEY (pt_id);


--
-- Name: resources resources_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.resources
    ADD CONSTRAINT resources_pkey PRIMARY KEY (resource_id);


--
-- Name: resources resources_resource_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.resources
    ADD CONSTRAINT resources_resource_name_key UNIQUE (resource_name);


--
-- Name: role_permissions role_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_pkey PRIMARY KEY (role_permission_id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (role_id);


--
-- Name: roles roles_role_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_role_name_key UNIQUE (role_name);


--
-- Name: sport sports_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sport
    ADD CONSTRAINT sports_name_key UNIQUE (sport_name);


--
-- Name: sport sports_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sport
    ADD CONSTRAINT sports_pkey PRIMARY KEY (sport_id);


--
-- Name: team team_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team
    ADD CONSTRAINT team_pkey PRIMARY KEY (team_id);


--
-- Name: team_tournament team_tournament_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team_tournament
    ADD CONSTRAINT team_tournament_pkey PRIMARY KEY (tt_id);


--
-- Name: tournament tournament_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tournament
    ADD CONSTRAINT tournament_pkey PRIMARY KEY (tournament_id);


--
-- Name: user_roles user_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_pkey PRIMARY KEY (user_role_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users users_user_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_user_email_key UNIQUE (user_email);


--
-- Name: action fk_action_sport; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.action
    ADD CONSTRAINT fk_action_sport FOREIGN KEY (sport_id) REFERENCES public.sport(sport_id) ON DELETE CASCADE;


--
-- Name: blog_person fk_bp_blog; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.blog_person
    ADD CONSTRAINT fk_bp_blog FOREIGN KEY (blog_id) REFERENCES public.blog(blog_id) ON DELETE CASCADE;


--
-- Name: blog_person fk_bp_person; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.blog_person
    ADD CONSTRAINT fk_bp_person FOREIGN KEY (person_id) REFERENCES public.person(person_id) ON DELETE CASCADE;


--
-- Name: blog_tournament fk_bt_blog; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.blog_tournament
    ADD CONSTRAINT fk_bt_blog FOREIGN KEY (blog_id) REFERENCES public.blog(blog_id) ON DELETE CASCADE;


--
-- Name: blog_tournament fk_bt_tournament; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.blog_tournament
    ADD CONSTRAINT fk_bt_tournament FOREIGN KEY (tournament_id) REFERENCES public.tournament(tournament_id) ON DELETE CASCADE;


--
-- Name: blog_team fk_bteam_blog; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.blog_team
    ADD CONSTRAINT fk_bteam_blog FOREIGN KEY (blog_id) REFERENCES public.blog(blog_id) ON DELETE CASCADE;


--
-- Name: blog_team fk_bteam_team; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.blog_team
    ADD CONSTRAINT fk_bteam_team FOREIGN KEY (team_id) REFERENCES public.team(team_id) ON DELETE CASCADE;


--
-- Name: game_actions fk_ga_action; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_actions
    ADD CONSTRAINT fk_ga_action FOREIGN KEY (action_id) REFERENCES public.action(action_id) ON DELETE RESTRICT;


--
-- Name: game_actions fk_ga_game; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_actions
    ADD CONSTRAINT fk_ga_game FOREIGN KEY (game_id) REFERENCES public.game(game_id) ON DELETE CASCADE;


--
-- Name: game_actions fk_ga_person; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_actions
    ADD CONSTRAINT fk_ga_person FOREIGN KEY (person_id) REFERENCES public.person(person_id) ON DELETE SET NULL;


--
-- Name: game_actions fk_ga_team; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_actions
    ADD CONSTRAINT fk_ga_team FOREIGN KEY (team_id) REFERENCES public.team(team_id) ON DELETE CASCADE;


--
-- Name: game fk_game_away_team; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game
    ADD CONSTRAINT fk_game_away_team FOREIGN KEY (away_team) REFERENCES public.team(team_id) ON DELETE RESTRICT;


--
-- Name: game fk_game_home_team; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game
    ADD CONSTRAINT fk_game_home_team FOREIGN KEY (home_team) REFERENCES public.team(team_id) ON DELETE RESTRICT;


--
-- Name: game fk_game_tournament; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game
    ADD CONSTRAINT fk_game_tournament FOREIGN KEY (tournament_id) REFERENCES public.tournament(tournament_id) ON DELETE CASCADE;


--
-- Name: lineup fk_lineup_game; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lineup
    ADD CONSTRAINT fk_lineup_game FOREIGN KEY (game_id) REFERENCES public.game(game_id) ON DELETE CASCADE;


--
-- Name: lineup fk_lineup_person; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lineup
    ADD CONSTRAINT fk_lineup_person FOREIGN KEY (person_id) REFERENCES public.person(person_id) ON DELETE CASCADE;


--
-- Name: lineup fk_lineup_team; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lineup
    ADD CONSTRAINT fk_lineup_team FOREIGN KEY (team_id) REFERENCES public.team(team_id) ON DELETE CASCADE;


--
-- Name: tournament fk_parent_tournament; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tournament
    ADD CONSTRAINT fk_parent_tournament FOREIGN KEY (parent_tournament_id) REFERENCES public.tournament(tournament_id) ON DELETE SET NULL;


--
-- Name: person_nationality fk_pnat_country; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person_nationality
    ADD CONSTRAINT fk_pnat_country FOREIGN KEY (country_id) REFERENCES public.country(country_id) ON DELETE CASCADE;


--
-- Name: person_nationality fk_pnat_person; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person_nationality
    ADD CONSTRAINT fk_pnat_person FOREIGN KEY (person_id) REFERENCES public.person(person_id) ON DELETE CASCADE;


--
-- Name: person_participation fk_pp_person_team; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person_participation
    ADD CONSTRAINT fk_pp_person_team FOREIGN KEY (pt_id) REFERENCES public.person_team(pt_id) ON DELETE CASCADE;


--
-- Name: person_participation fk_pp_team_tournament; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person_participation
    ADD CONSTRAINT fk_pp_team_tournament FOREIGN KEY (tt_id) REFERENCES public.team_tournament(tt_id) ON DELETE CASCADE;


--
-- Name: person_team fk_pt_person; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person_team
    ADD CONSTRAINT fk_pt_person FOREIGN KEY (person_id) REFERENCES public.person(person_id) ON DELETE CASCADE;


--
-- Name: person_team fk_pt_team; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person_team
    ADD CONSTRAINT fk_pt_team FOREIGN KEY (team_id) REFERENCES public.team(team_id) ON DELETE CASCADE;


--
-- Name: tournament fk_sport; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tournament
    ADD CONSTRAINT fk_sport FOREIGN KEY (sport_id) REFERENCES public.sport(sport_id) ON DELETE CASCADE;


--
-- Name: team fk_team_country; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team
    ADD CONSTRAINT fk_team_country FOREIGN KEY (country_id) REFERENCES public.country(country_id) ON DELETE RESTRICT;


--
-- Name: team fk_team_sport; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team
    ADD CONSTRAINT fk_team_sport FOREIGN KEY (sport_id) REFERENCES public.sport(sport_id) ON DELETE CASCADE;


--
-- Name: team_tournament fk_tt_team; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team_tournament
    ADD CONSTRAINT fk_tt_team FOREIGN KEY (team_id) REFERENCES public.team(team_id) ON DELETE CASCADE;


--
-- Name: team_tournament fk_tt_tournament; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team_tournament
    ADD CONSTRAINT fk_tt_tournament FOREIGN KEY (tournament_id) REFERENCES public.tournament(tournament_id) ON DELETE CASCADE;


--
-- Name: permissions permissions_auth_action_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_auth_action_id_fkey FOREIGN KEY (auth_action_id) REFERENCES public.auth_actions(auth_action_id);


--
-- Name: permissions permissions_resource_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES public.resources(resource_id);


--
-- Name: role_permissions role_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.permissions(permission_id);


--
-- Name: role_permissions role_permissions_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(role_id);


--
-- Name: user_roles user_roles_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organization(organization_id);


--
-- Name: user_roles user_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(role_id);


--
-- Name: user_roles user_roles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: users users_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organization(organization_id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT ALL ON SCHEMA public TO skwod_api_dev_user;


--
-- Name: TABLE action; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.action TO skwod_api_dev_user;


--
-- Name: TABLE auth_actions; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.auth_actions TO skwod_api_dev_user;


--
-- Name: TABLE blog; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.blog TO skwod_api_dev_user;


--
-- Name: TABLE blog_person; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.blog_person TO skwod_api_dev_user;


--
-- Name: TABLE blog_team; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.blog_team TO skwod_api_dev_user;


--
-- Name: TABLE blog_tournament; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.blog_tournament TO skwod_api_dev_user;


--
-- Name: TABLE country; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.country TO skwod_api_dev_user;


--
-- Name: TABLE game; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.game TO skwod_api_dev_user;


--
-- Name: TABLE game_actions; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.game_actions TO skwod_api_dev_user;


--
-- Name: TABLE lineup; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.lineup TO skwod_api_dev_user;


--
-- Name: TABLE organization; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.organization TO skwod_api_dev_user;


--
-- Name: TABLE permissions; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.permissions TO skwod_api_dev_user;


--
-- Name: TABLE person; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.person TO skwod_api_dev_user;


--
-- Name: TABLE person_nationality; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.person_nationality TO skwod_api_dev_user;


--
-- Name: TABLE person_participation; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.person_participation TO skwod_api_dev_user;


--
-- Name: TABLE person_team; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.person_team TO skwod_api_dev_user;


--
-- Name: TABLE resources; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.resources TO skwod_api_dev_user;


--
-- Name: TABLE role_permissions; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.role_permissions TO skwod_api_dev_user;


--
-- Name: TABLE roles; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.roles TO skwod_api_dev_user;


--
-- Name: TABLE sport; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.sport TO skwod_api_dev_user;


--
-- Name: TABLE team; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.team TO skwod_api_dev_user;


--
-- Name: TABLE team_tournament; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.team_tournament TO skwod_api_dev_user;


--
-- Name: TABLE tournament; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.tournament TO skwod_api_dev_user;


--
-- Name: TABLE user_roles; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.user_roles TO skwod_api_dev_user;


--
-- Name: TABLE users; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.users TO skwod_api_dev_user;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT SELECT,INSERT,DELETE,UPDATE ON TABLES TO skwod_api_dev_user;


--
-- PostgreSQL database dump complete
--

\unrestrict gVKRd2hQvfGCarl0ptatB9h4wMIkE2op7DVKt02A6RIKTAYR1PTF7Q4eyLsTbaV

