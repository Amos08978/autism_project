--
-- PostgreSQL database dump
--

\restrict Z4N0leWVzk2vfqkH6ehBALOQvWuEY3b0VvIR9dETlSKe2zXeGielOX2gkMx71YF

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: accounts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts (
    id integer NOT NULL,
    parent_name character varying(100) NOT NULL,
    child_name character varying(100) NOT NULL,
    child_age integer NOT NULL,
    phone character varying(20),
    address character varying(200),
    email character varying(100),
    line character varying(100),
    privacy_signed_at timestamp without time zone
);


ALTER TABLE public.accounts OWNER TO postgres;

--
-- Name: accounts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.accounts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.accounts_id_seq OWNER TO postgres;

--
-- Name: accounts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.accounts_id_seq OWNED BY public.accounts.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: autism_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO autism_user;

--
-- Name: expression_images; Type: TABLE; Schema: public; Owner: autism_user
--

CREATE TABLE public.expression_images (
    id integer NOT NULL,
    type_id integer NOT NULL,
    stage character varying(20) NOT NULL,
    image_path character varying(200) NOT NULL
);


ALTER TABLE public.expression_images OWNER TO autism_user;

--
-- Name: expression_images_id_seq; Type: SEQUENCE; Schema: public; Owner: autism_user
--

CREATE SEQUENCE public.expression_images_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.expression_images_id_seq OWNER TO autism_user;

--
-- Name: expression_images_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: autism_user
--

ALTER SEQUENCE public.expression_images_id_seq OWNED BY public.expression_images.id;


--
-- Name: expression_types; Type: TABLE; Schema: public; Owner: autism_user
--

CREATE TABLE public.expression_types (
    id integer NOT NULL,
    type_name character varying(50) NOT NULL,
    image_path character varying(200)
);


ALTER TABLE public.expression_types OWNER TO autism_user;

--
-- Name: expression_types_id_seq; Type: SEQUENCE; Schema: public; Owner: autism_user
--

CREATE SEQUENCE public.expression_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.expression_types_id_seq OWNER TO autism_user;

--
-- Name: expression_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: autism_user
--

ALTER SEQUENCE public.expression_types_id_seq OWNED BY public.expression_types.id;


--
-- Name: loginlog; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.loginlog (
    id integer NOT NULL,
    account_id integer,
    login_result character varying(20) NOT NULL,
    reason character varying(200),
    login_datetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.loginlog OWNER TO postgres;

--
-- Name: loginlog_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.loginlog_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.loginlog_id_seq OWNER TO postgres;

--
-- Name: loginlog_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.loginlog_id_seq OWNED BY public.loginlog.id;


--
-- Name: testresults; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.testresults (
    id integer NOT NULL,
    account_id integer,
    stage character varying(20) NOT NULL,
    child_choice character varying(20) NOT NULL,
    system_result character varying(5) NOT NULL,
    test_datetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    image_id integer,
    batch_id character varying(50)
);


ALTER TABLE public.testresults OWNER TO postgres;

--
-- Name: testresults_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.testresults_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.testresults_id_seq OWNER TO postgres;

--
-- Name: testresults_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.testresults_id_seq OWNED BY public.testresults.id;


--
-- Name: accounts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts ALTER COLUMN id SET DEFAULT nextval('public.accounts_id_seq'::regclass);


--
-- Name: expression_images id; Type: DEFAULT; Schema: public; Owner: autism_user
--

ALTER TABLE ONLY public.expression_images ALTER COLUMN id SET DEFAULT nextval('public.expression_images_id_seq'::regclass);


--
-- Name: expression_types id; Type: DEFAULT; Schema: public; Owner: autism_user
--

ALTER TABLE ONLY public.expression_types ALTER COLUMN id SET DEFAULT nextval('public.expression_types_id_seq'::regclass);


--
-- Name: loginlog id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loginlog ALTER COLUMN id SET DEFAULT nextval('public.loginlog_id_seq'::regclass);


--
-- Name: testresults id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.testresults ALTER COLUMN id SET DEFAULT nextval('public.testresults_id_seq'::regclass);


--
-- Name: accounts accounts_parent_name_child_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_parent_name_child_name_key UNIQUE (parent_name, child_name);


--
-- Name: accounts accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: autism_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: expression_images expression_images_pkey; Type: CONSTRAINT; Schema: public; Owner: autism_user
--

ALTER TABLE ONLY public.expression_images
    ADD CONSTRAINT expression_images_pkey PRIMARY KEY (id);


--
-- Name: expression_types expression_types_pkey; Type: CONSTRAINT; Schema: public; Owner: autism_user
--

ALTER TABLE ONLY public.expression_types
    ADD CONSTRAINT expression_types_pkey PRIMARY KEY (id);


--
-- Name: expression_types expression_types_type_name_key; Type: CONSTRAINT; Schema: public; Owner: autism_user
--

ALTER TABLE ONLY public.expression_types
    ADD CONSTRAINT expression_types_type_name_key UNIQUE (type_name);


--
-- Name: loginlog loginlog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loginlog
    ADD CONSTRAINT loginlog_pkey PRIMARY KEY (id);


--
-- Name: testresults testresults_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.testresults
    ADD CONSTRAINT testresults_pkey PRIMARY KEY (id);


--
-- Name: ix_expression_images_id; Type: INDEX; Schema: public; Owner: autism_user
--

CREATE INDEX ix_expression_images_id ON public.expression_images USING btree (id);


--
-- Name: ix_expression_types_id; Type: INDEX; Schema: public; Owner: autism_user
--

CREATE INDEX ix_expression_types_id ON public.expression_types USING btree (id);


--
-- Name: expression_images expression_images_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: autism_user
--

ALTER TABLE ONLY public.expression_images
    ADD CONSTRAINT expression_images_type_id_fkey FOREIGN KEY (type_id) REFERENCES public.expression_types(id);


--
-- Name: loginlog loginlog_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loginlog
    ADD CONSTRAINT loginlog_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.accounts(id) ON DELETE CASCADE;


--
-- Name: testresults testresults_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.testresults
    ADD CONSTRAINT testresults_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.accounts(id) ON DELETE CASCADE;


--
-- Name: testresults testresults_image_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.testresults
    ADD CONSTRAINT testresults_image_id_fkey FOREIGN KEY (image_id) REFERENCES public.expression_images(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT ALL ON SCHEMA public TO autism_user;


--
-- Name: TABLE accounts; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.accounts TO autism_user;


--
-- Name: SEQUENCE accounts_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.accounts_id_seq TO autism_user;


--
-- Name: TABLE loginlog; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.loginlog TO autism_user;


--
-- Name: SEQUENCE loginlog_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.loginlog_id_seq TO autism_user;


--
-- Name: TABLE testresults; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.testresults TO autism_user;


--
-- Name: SEQUENCE testresults_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.testresults_id_seq TO autism_user;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON TABLES TO autism_user;


--
-- PostgreSQL database dump complete
--

\unrestrict Z4N0leWVzk2vfqkH6ehBALOQvWuEY3b0VvIR9dETlSKe2zXeGielOX2gkMx71YF

