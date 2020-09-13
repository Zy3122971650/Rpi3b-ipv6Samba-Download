function post_data() {
    var form = document.getElementById('forml')
    var formData = new FormData(form)
    var host = document.getElementById('host').value
    var xhr = new XMLHttpRequest()
    xhr.open('POST', 'http://' + host + ':8002/download', false)
    xhr.send(formData)
};

function get_download_info() {
    function get(from) {
        var host = document.getElementById('host').value
        var url = `http://${host}:8002/download/${from}`
        var xhr = new XMLHttpRequest()
        xhr.open('GET', url, true)
        xhr.send(null)
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                write(from, xhr.responseText)
            }
        }
    }
    function write(id, data) {
        var dom = document.getElementById(id)
        if (id == 'info') {
            var i = 3
            data = JSON.parse(data)
            var h = []
            h.push("<table cellspacing='30'>")
            h.push("<th>文件名</th><th>下载进度</th><th>速度</th>")
            for (var key in data) {
                data_temp = data[key]
                var size = data_temp['size']
                var total_size = data_temp['total_size']
                var title = data_temp['title']
                var speed = 0
                h.push(`<tr><td>${title}</td><td><progress id='bar${key}' max='${total_size}' value='${size}'></progress></td><td>${speed}</td></tr>`)
                i = i-1
            }
            if (i != 3){
                h.push('</table>')
                dom.innerHTML = h.join("")
            }else{
                dom.innerHTML  = "<p>没有下载正在进行哦......</p>"
            }

        } else {
            
            var h = []
            h.push("<table cellspacing='30'>")
            if (id == 'wait_lst'){
                h.push("<th>序号</th><th>文件名</th><th>下载参数</th>")
            }else{
                h.push("<th>序号</th><th>下载参数</th>")
            }
            data = JSON.parse(data)
            var i = 0
            for (var key in data){
                i　= i + 1
                data_temp = data[key]
                if (id == 'waitInfo'){
                    h.push(`<tr><td>${i}</td><td>${data_temp['args']}</td></tr>`)
                }else{
                    h.push(`<tr><td>${i}</td><td>${data_temp['title']}</td><td>${data_temp['origin']}</td></tr>`)
                }
            }
            if (i!=0){
                h.push('</table>')
                dom.innerHTML = h.join("")
            }else{
                if (id = 'waitInfo'){
                    dom.innerHTML = "<p>等待列表没有任务......</p>"
                }else{
                    dom.innerHTML = "<p>从运行开始还没有任务完成被哦......</p>"

                }
                
            }
        }
    }
    function main() {
        get('info')
        get('waitInfo')
        get('cpltInfo')
    
    }
    setInterval(main,500)
};


