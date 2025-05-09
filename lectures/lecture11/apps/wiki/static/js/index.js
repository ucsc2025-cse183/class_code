"use strict";

function clone(obj) { return JSON.parse(JSON.stringify(obj)); }

let app = {}
app.converter = new showdown.Converter();
app.config = {
    data: function() {
        return {
            edit_mode: false,
            page: {
                title: "my title",
                content: "hello world", 
            },
            comments: [
                {content: "nice!"},
                {content: "bad!"}
            ]
        };
    },
    methods: {   
        converted: function(md) { return app.converter.makeHtml(md);},
        save: function() {
            fetch("/wiki/api/page",
                {
                    headers: {
                      'Accept': 'application/json',
                      'Content-Type': 'application/json'
                    },
                    method: "POST",
                    body: JSON.stringify(app.vue.page)
                })
        }
    }
};

app.vue = Vue.createApp(app.config).mount("#app");
