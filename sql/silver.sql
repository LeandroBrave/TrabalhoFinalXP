CREATE TABLE silver.dadostesouroipca (
	compra float8 NOT NULL,
	venda float8 NOT NULL,
	pu_compra float8 NOT NULL,
	pu_venda float8 NOT NULL,
	pu_base float8 NOT NULL,
	data_vencimento date NULL,
	data_base date NULL,
	tipo text NULL,
	dt_update date NULL
);


CREATE TABLE silver.dadostesouropre (
	compra float8 NOT NULL,
	venda float8 NOT NULL,
	pu_compra float8 NOT NULL,
	pu_venda float8 NOT NULL,
	pu_base float8 NOT NULL,
	data_vencimento date NULL,
	data_base date NULL,
	tipo text NULL,
	dt_update date NULL
);