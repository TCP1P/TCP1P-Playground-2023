{{template "../header.tpl"}}
<main class="container">
    <section class="row mt-5">
        <div class="col-12 text-center">
            <h1>Regular Note App</h1>
        </div>
        <div class="col-12">
            {{.Note.Value}}
        </div>
    </section>
</main>
{{template "../footer.tpl"}}