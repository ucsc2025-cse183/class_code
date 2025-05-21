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
    


let app = {}
app.empty_new_bird = {"id": 0, "name": "", "habitat": "", "weight": 0, "sightings": 0},
app.config = {
    data: function() {
        return {
            error_message: "",
            new_bird: clone(app.empty_new_bird),            
            birds: [],
            selected_birds: [],
            editing: {current: null}
        };
    },
    methods: {       
        search: function() {
            this.cancel();
            this.selected_birds = this.birds.filter((bird)=>{return bird.name.toLowerCase().includes(this.new_bird.name.toLowerCase()); });
        },
        add_bird: function() {
            this.cancel();
            if (this.selected_birds.length==0 && this.new_bird.name.length>1) {
                let bird = clone(this.new_bird);
                this.birds.push(bird);
                this.new_bird = app.empty_new_bird;
                this.selected_birds = [bird];
                ajax("/bird_spotter/api/birds", "POST", bird).then(function(res){
                    if (res.errors && Object.keys(res.errors).length>0) {
                        app.vue.error_message = JSON.stringify(res.errors);
                    } else {
                        bird.id = res.id;
                    }
                });
            }            
        },
        edit: function(bird) {
            this.cancel();
            this.editing = {current: bird, old: clone(bird)};
        },
        save: function(bird) {
            bird = clone(bird);
            let url = "/bird_spotter/api/birds/" + bird.id;
            delete bird.id;
            delete bird.name;
            // PUT bird to /bird_spotter/api/birds/{bird.id}            
            ajax(url, "PUT", bird).then(function(res){
                if(res.errors && Object.keys(res.errors).length>0) {
                    app.vue.error_message = JSON.stringify(res.errors);
                } else {
                    app.vue.error_message = "";
                    app.vue.editing = {current: null};
                }
            });
        },
        cancel: function() {
            if (this.editing.current)
                for(var key in this.editing.current)
                    this.editing.current[key] = this.editing.old[key];
            this.editing = {current: null};
        },
        add_sighting: function(bird) {
            bird.sightings += 1;
            ajax("/bird_spotter/api/birds/" + bird.id + "/increase_sightings", "POST", {});
        },
        color: function(name) {            
            let hash = 0;
            for (let i = 0; i < name.length; i++) hash = name.charCodeAt(i) + ((hash << 5) - hash);            
            let ret = `hsl(${(hash % 360)}, 100%, 75%)`;                         
            console.log(ret);
            return ret;
        },
    }
};

app.load_data = function() {
    ajax("/bird_spotter/api/birds", "GET").then(function(res){
        app.vue.birds = res.birds;
        app.vue.search();
    });
}

app.vue = Vue.createApp(app.config).mount("#app");
app.load_data();
