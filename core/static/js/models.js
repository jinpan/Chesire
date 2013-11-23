var QuestionAnswer = Backbone.Model.extend({
    defaults: {
        question: 'Why is the sky blue?',
        answer: 'Because.',
        original_url: 'http://jinpan.mit.edu',
        source: 'thin air',
        state: 'question',
        display_text: 'Why is the sky blue?'
    },
    initialize: function(){
        this.on('change:state', function(model){
            var state = model.get('state');
            model.set({
                display_text: model.get(state)
            });
        });
    },
    swap_state: function(){
        if (this.get('state') === 'question'){
            this.set({
                state: 'answer'
            });
        }
        else {
            this.set({
                state: 'question'
            });
        }
    }
});
