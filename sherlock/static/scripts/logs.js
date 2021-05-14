class Logs {
    constructor() {
        this.logsWrapper = document.getElementById('network-logs');
        this.logs = document.getElementById('network-logs-container');
        this.btn = document.getElementById('hide-logs');
        this.logsTitle = document.getElementById('network-logs-ip-address');

        this.btn.addEventListener('click', function(e) {
            this.setVisibility(false);
            this.logsTitle.innerText = "";
            this.logs.innerHTML = "";
        }.bind(this), false );


        this.visibility = false;
        this.ip = null;
    }

    addLogs(logs) {
        this.logs.innerHTML = "<br/>" + logs;
    }

    setVisibility(visibility) {
        if (visibility) {
            this.logsWrapper.classList.add('visible')
        } else {
            this.logsWrapper.classList.remove('visible')
        }

        this.visibility = visibility;
    }

    isVisible() {
        return this.visibility;
    }

    getIp() {
        return this.ip;
    }

    setIp(ip) {
        this.ip = ip;
    }

    addPacket(packet) {
        this.logs.innerHTML += `<div style="padding-bottom: 10px;">`;
        this.logs.innerHTML += `<p style="font-weight: bold; color: antiquewhite;">` + packet.source_ip_address + ":" + packet.source_port + " -> " + packet.destination_ip_address + ":" + packet.destination_port + "</p>";
        this.logs.innerHTML += `<p style="font-weight: bold; color: antiquewhite;">` + packet.protocol + "</p>";
        this.logs.innerHTML += "<p>" + packet.payload + "</p>";
        this.logs.innerHTML += "</div>";
        this.scrollToBottom();
    }

    scrollToBottom() {
        const logs = $(`#${this.logs.id}`);
        logs.stop().animate({
            scrollTop: logs[0].scrollHeight - logs[0].clientHeight
        }, 500);
    }

}