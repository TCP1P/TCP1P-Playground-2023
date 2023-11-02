package controllers

import (
	"encoding/json"
	beego "github.com/beego/beego/v2/server/web"
	"src/models"
	"strconv"
)

type NoteController struct {
	beego.Controller
}

func (c *NoteController) URLMapping() {
	c.Mapping("Post", c.noteMiddleWare(c.Post))
}

func (c *NoteController) noteMiddleWare(f func()) func() {
	var note map[string]interface{}
	err := json.Unmarshal(c.Ctx.Input.RequestBody, &note)
	if err != nil {
		c.CustomAbort(500, err.Error())
	}
	if note["IsAdmin"] == nil || note["Id"] == nil {
		c.CustomAbort(400, "Bad Requests")
	}
	if note["IsAdmin"] == true {
		c.CustomAbort(403, "We didn't allow that!")
	}
	return f
}

func (c *NoteController) Post() {
	var note models.Note
	err := c.Bind(&note)
	if err != nil {
		c.CustomAbort(500, err.Error())
	}
	if note.IsAdmin != true {
		c.CustomAbort(403, "Access Denied")
	}
	var noteId string
	switch note.Id.(type) {
	case float64:
		noteId = strconv.Itoa(int(note.Id.(float64)))
		break
	case string:
		noteId = note.Id.(string)
	}
	notevalue, err := models.GetNote(noteId)
	if err != nil {
		c.CustomAbort(500, err.Error())
	}
	c.Data["Note"] = notevalue
}
