CREATE TABLE gold.dim_tempo (
	"data" date not NULL,
	ano int4 NULL,
	mes int4 NULL,
	nome_mes text NULL,
	dia int4 NULL,
	dia_da_semana int4 NULL,
	nome_dia_semana text NULL,
	semana_do_ano int8 NULL,
	trimestre int4 NULL,
	eh_fim_de_semana bool NULL,
	ano_mes text NULL,
	--id_data int8 not NULL,
	eh_feriado bool null
);

ALTER TABLE gold.dim_tempo
ADD CONSTRAINT dim_tempo_pkey PRIMARY KEY ("data");

CREATE TABLE gold.dim_tipo (
	id_tipo serial4 NOT NULL,
	tipo text NOT NULL,
	CONSTRAINT dim_tipo_pkey PRIMARY KEY (id_tipo)
);


ALTER TABLE gold.dim_tipo
ADD CONSTRAINT dim_tipo_ukey UNIQUE (tipo);

CREATE TABLE gold.fato_dadostesouro_base (
    id_fato SERIAL PRIMARY KEY,
    data_base_ano_mes text NOT NULL,
    id_tipo INT NOT NULL,
    compra FLOAT8 NOT NULL,
    venda FLOAT8 NOT NULL,
    pu_compra FLOAT8 NOT NULL,
    pu_venda FLOAT8 NOT NULL,
    pu_base FLOAT8 NOT NULL,
    dt_update TIMESTAMP,
    CONSTRAINT fk_tipo FOREIGN KEY (id_tipo)
        REFERENCES gold.dim_tipo(id_tipo)
);

CREATE TABLE gold.fato_dadostesouro_venc (
    id_fato SERIAL PRIMARY KEY,
    data_vencimento_ano_mes text NOT NULL,
    id_tipo INT NOT NULL,
    compra FLOAT8 NOT NULL,
    venda FLOAT8 NOT NULL,
    pu_compra FLOAT8 NOT NULL,
    pu_venda FLOAT8 NOT NULL,
    pu_base FLOAT8 NOT NULL,
    dt_update TIMESTAMP,
    CONSTRAINT fk_tipo FOREIGN KEY (id_tipo)
        REFERENCES gold.dim_tipo(id_tipo)
);
