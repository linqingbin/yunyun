var botui = new BotUI('hello-world');

var messages = {
    'theme':'请输入本次思考的主题',
    'compare':'请输入要对比的对象（逗号分隔每个对象）'
}
var human_input = function (){
    return botui.action.text({
        action: {placeholder: '请输入'}
    });
}

var robot_ask = function(message){
    return botui.message.bot({content:message})
}

var loop_input = function(range,res_values=[]){
    if (range.length){
        robot_ask("对于"+range[0]+"，你觉得权重有多大，请在-2,-1,0,1,2中选择")
        .then(human_input)
        .then(function(res){
            res_values.push(res.value);
            // console.info(res_values)
            return loop_input(range.slice(1,),res_values)
        });
    }
    else{
        console.info(res_values)
        return res_values
    }            
}

var add = function(){
    return 1
}
var feature_weights = []
var title = ''
robot_ask(messages['theme']).then(human_input).then(
    function (res) {
        
        var title = res.value;
        robot_ask(messages['compare']);
    })
    .then(human_input)
    .then(function (res) {
            var result = {}
            var compare_vars = res.value.split(',')
            var x = loop_input(compare_vars,[])
            
            // 可能因为在递归中存在中断执行，使得递归无法正常传值
            })
    .then(function(){return robot_ask('等待新的输入')})
