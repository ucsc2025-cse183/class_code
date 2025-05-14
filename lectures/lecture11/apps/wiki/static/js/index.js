"use strict";

function clone(obj) { return JSON.parse(JSON.stringify(obj)); }

function ajax(url, method, data) {
    let options = {
        method: method,
        headers: { 'Content-Type': 'application/json' }
    };
    if (data) {
        options.body = JSON.stringify(data);
    }
    return fetch(url, options).then(response => { return response.json(); });
}

function get_page_id() {
    let parts = document.location.pathname.split("/");
    return parseInt(parts[parts.length-1]) || null;
}

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
            let page_id = get_page_id();
            if (!page_id)
            {                
                ajax("/wiki/api/page", "POST", app.vue.page).then(function(res){
                    // console.log(res);
                    window.location = "/wiki/" + res.id;
                });
            } else {
                ajax("/wiki/api/page/" + page_id, "PUT", app.vue.page);
            }
        }
    }
};

app.vue = Vue.createApp(app.config).mount("#app");

let page_id = get_page_id();
if (page_id) {
    ajax("/wiki/api/page/" + page_id, "GET").then(function(res){
        app.vue.page = res.page;
    });
    ajax("/wiki/api/page/" + page_id + "/comment", "GET").then(function(res){
        app.vue.comments = res.comments;
    });
}
