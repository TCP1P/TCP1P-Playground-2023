package routers

import (
	beego "github.com/beego/beego/v2/server/web"
	"src/controllers"
)

func init() {
	beego.Router("/", &controllers.MainController{})
	beego.Router("/note", &controllers.NoteController{})
}
