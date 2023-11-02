package models

import (
	"database/sql"
	"fmt"
	"os"

	_ "github.com/go-sql-driver/mysql"
)

type Note struct {
	Id      interface{}
	Value   string
	IsAdmin bool
}

func koneksi() *sql.DB {
	// example: root:passwd@tcp(localhost:3306)/notedb
	dataSource := os.Getenv("DATASRC")
	open, err := sql.Open("mysql", dataSource)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	if err = open.Ping(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	return open
}

func GetNote(id string) (Note, error) {
	db := koneksi()
	fmt.Println(`SELECT * FROM notes WHERE id=` + id)
	row := db.QueryRow(`SELECT * FROM notes WHERE id=` + id)
	var note Note
	if err := row.Scan(&note.Id, &note.Value, &note.IsAdmin); err != nil {
		return Note{}, err
	}
	return note, nil
}
