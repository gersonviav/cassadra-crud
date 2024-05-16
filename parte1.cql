-- Export of keyspace practica2
CREATE KEYSPACE gersonvillugas
WITH durable_writes = true AND replication = {'class' : 'SimpleStrategy', 'replication_factor' : 1};

CREATE TABLE gersonvillugas.tabla1 (
	Libro_anio int,
	Libro_ISBN text,
	Libro_titulo text,
	PRIMARY KEY (Libro_anio, Libro_ISBN)
) WITH CLUSTERING ORDER BY ( Libro_ISBN ASC );

 
CREATE TABLE gersonvillugas.tabla2 (
	Libro_titulo text,
	Ejemplar_nro int,
	Ejemplar_status text,
	PRIMARY KEY (Libro_titulo, Ejemplar_nro)
) WITH CLUSTERING ORDER BY ( Ejemplar_nro ASC );


CREATE TABLE gersonvillugas.tabla3 (
	Autor_nombre text,
	Autor_cod int,
	Libro_ISBN text,
	Libro_titulo text,
	Libro_anio text,
	
	PRIMARY KEY (Autor_nombre, Autor_cod,Libro_ISBN)
) WITH CLUSTERING ORDER BY ( Autor_cod ASC );

CREATE TABLE gersonvillugas.tabla4 (
	Libro_titulo text,
	Usuario_DNI text,
	Ejemplar_nro int,
	Usuario_nombre text,
	Usuario_calle text,
	Usuario_ciudad text,
	PRIMARY KEY (Libro_titulo, Usuario_DNI)
) WITH CLUSTERING ORDER BY ( Usuario_DNI ASC );
create table gersonvillugas.tabla5
( Usuario_ciudad text,
  Usuario_DNI text,
  Usuario_nombre text,
  Usuario_calle text,
  primary key ((Usuario_ciudad,Usuario_DNI))
);
CREATE TABLE gersonvillugas.tabla6 (
	Ejemplar_nro int,
	NumPrestamos counter,
	PRIMARY KEY (Ejemplar_nro)
);
CREATE TABLE gersonvillugas.tabla7 (
	Autor_premio text,
	Autor_cod int,
	Autor_nombre text,
	Autor_premios SET<text>,
	PRIMARY KEY (Autor_premio, Autor_cod)
) WITH CLUSTERING ORDER BY ( Autor_cod ASC );

CREATE TABLE gersonvillugas.tabla8 (
	Es_prestado date,
	Ejemplar_nro int,
	Usuario_DNI text,
	Usuario_nombre text,
	PRIMARY KEY (Es_prestado, Ejemplar_nro,Usuario_DNI)
) WITH CLUSTERING ORDER BY ( Ejemplar_nro  ASC );


---- TABLAS SOPORTE

CREATE TABLE gersonvillugas.SoporteLibro
(
  Libro_ISBN text,
  Libro_titulo text,
  Libro_anio int,
  Libro_temas SET<text>,
  PRIMARY KEY (Libro_ISBN)
) ;
CREATE TABLE gersonvillugas.SoporteUsuario
(
  Usuario_DNI text,
  Usuario_nombre text,
  Usuario_calle text,
  Usuario_ciudad text,
  PRIMARY KEY (Usuario_DNI)
) ;


CREATE TABLE gersonvillugas.Ejemplar_Usuario
(
	 Ejemplar_status text,
	 Ejemplar_nro int, 
	 Es_prestado date,
	 Usuario_DNI text, 
	 Usuario_nombre text, 
	 Usuario_calle text,
	 Usuario_ciudad text,
	PRIMARY KEY (Es_prestado,Ejemplar_nro,Usuario_DNI)
);


CREATE TABLE gersonvillugas.Libro_Ejemplar
(
	 Ejemplar_status text,
	 Ejemplar_nro int, 
	 Es_prestado date,
	 Libro_ISBN text, 
	 Libro_titulo text, 
	 Libro_anio text,
	PRIMARY KEY (Es_prestado,Ejemplar_nro)
);


CREATE TABLE gersonvillugas.Libro_Usuario
(
	 Usuario_DNI text,
	 Usuario_nombre text, 
	 Usuario_calle text,
	 Usuario_ciudad text, 
	 Libro_ISBN text, 
	 Libro_titulo text, 
	 Libro_anio text,
	PRIMARY KEY (Usuario_DNI)
);

