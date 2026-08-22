'use strict'
import { writeFile } from "fs";

export default function (app, opts) {
  // Setup routes, middleware, and handlers
  app.get('/', (req, res) => {
    res.locals.name = 'src'
    res.render('index')
  })
  app.get("/:page", (req,res)=>{
    res.render(req.params.page)
  })
  app.get("/note/:id", (req,res)=>{
    res.sendfile(`./storage/${req.params.id}.html`)
  })
  app.post("/note", (req,res)=>{
    let {note} = req.body
    note = `<html lang="en">
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" >
    <title>Your Note</title>
</head>
<body>
    <div class="container">
        <div class="d-flex flex-row justify-content-center m-5">
            ${note}
        </div>
    </div>
</body>
</html>`
    const filename = crypto.randomUUID()
    writeFile(`./storage/${filename}.html`, note, (err)=>{
      if (err){
        throw err
      }else{
        res.redirect(`/note/${filename}`)
      }
    })
  })
}
