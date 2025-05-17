"use strict";

function clone(obj) { return JSON.parse(JSON.stringify(obj)); }

function ajax(url, method, data, callback) {
    let options = {
        method: method,
        headers: { 'Content-Type': 'application/json' }
    };
    if (data) {
        options.body = JSON.stringify(data);
    }
    return fetch(url, options).then(response => { return response.json(); }).then(function(res){
        if(res.errors && res.errors.length) {
            console.log(res);
            alert("validation error " + JSON.stringify(res.errors));
        } else if (callback) {
            callback(res);
        }
    }, function(){ alert("network error"); });
}

function get_page_id() {
    let parts = document.location.pathname.split("/");
    return parseInt(parts[parts.length-1]) || null;
}

let app = {};
app.converter = new showdown.Converter();
app.config = {
    data: function() {
        return {
            edit_mode: false,       
            pages: [],     
            page: {
                id: get_page_id(),
                title: "my title",
                content: "hello world", 
            },
            comments: [
                {content: "nice!"},
                {content: "bad!"}
            ],
            new_comment: ""
        };
    },
    methods: {   
        converted: function(md) { return app.converter.makeHtml(md);},
        toggle_edit_mode: function() {
            app.vue.edit_mode = !app.vue.edit_mode;
        },
        save: function() {
            let data = {
                "title": app.vue.page.title, 
                "content": app.vue.page.content
            };
            if (!app.vue.page.id)
            {   
                ajax("/wiki/api/page", "POST", data, function(res){
                    window.location = "/wiki/page/" + res.id;                    
                });
            } else {
                ajax("/wiki/api/page/" + app.vue.page.id, "PUT", data, function(res){
                    app.vue.edit_mode = false;
                });
            }
        },
        delete_page: function() {
            if (confirm("sure you want to delete?")) {
                ajax("/wiki/api/page/"+app.vue.page.id, "DELETE", null, function(res){
                    alert("delete");
                    window.location = "/wiki/index";                   
                });
            }
        },
        post_comment: function() {
            let comment = {"content": app.vue.new_comment};
            ajax("/wiki/api/page/"+app.vue.page.id+"/comment", "POST", comment,function(res){
                app.vue.comments.push(comment);
                app.vue.new_comment = "";
            });
        },
        load_everything: function() {
            ajax("/wiki/api/page", "GET", null, function(res){
                app.vue.pages = res.pages;
            });
            if (app.vue.page.id) {
                ajax("/wiki/api/page/" + app.vue.page.id, "GET", null, function(res){
                    app.vue.page = res.page;
                });
                ajax("/wiki/api/page/" + app.vue.page.id + "/comment", "GET", null, function(res){
                    app.vue.comments = res.comments;
                });
            }            
        }
    }
};

app.vue = Vue.createApp(app.config).mount("#app");
app.vue.load_everything();
