import React, { Component } from 'react'
import { Launcher } from 'react-chat-window'
import customerCare from '../../Assets/customer-care.png'
import { w3cwebsocket as W3CWebSocket } from 'websocket';
import Axios from 'axios';
import { InvigilatorContext } from '../../Context/InvigilatorContext';
import { wsUrl } from '../../config';

class ChatModal extends Component {
    static contextType = InvigilatorContext;
    constructor(props) {
        super(props);
        this.state = {
            Client1: null,
            Client2: null,
            messageList: [],
            invigilator: null
        };
    }

    componentDidUpdate(prevProps) {
        if (prevProps.invigilator !== this.state.invigilator) {
            this.setState({ invigilator: prevProps.invigilator });
        }
    }

    componentWillMount() {
        const { invigilator, clientId } = this.context;
        this.setState({
            Client1: new W3CWebSocket(`${wsUrl}/invigilator/chat/${invigilator}_${clientId}`),
            Client2: new W3CWebSocket(`${wsUrl}/invigilator/chat/${invigilator}/Client`),
        })
    }

    componentDidMount() {
        const { invigilator, clientId } = this.context;
        const { Client1, Client2 } = this.state;
        Axios.get(`/invigilator/get-invigilator-client-chat/${invigilator}/${clientId}`).then((res) => {
            const messages = [];
            res.data.results.map((item) => {
                let author;
                if (item.message_from === "Invigilator") {
                    author = "them";
                }
                else {
                    author = "me"
                }
                return messages.push({
                    author: author,
                    type: "text",
                    data: {
                        text: item.message
                    }
                })
            });
            this.setState({ messageList: messages.reverse() })
        });

        Client1.onopen = () => {
            console.log('Hey i will be interacting');
        };

        Client2.onopen = () => {

        }

        Client1.onmessage = (message) => {
            const messages = [...this.state.messageList];
            let author;
            const temp = JSON.parse(message.data);
            if (temp.from === "Invigilator") {
                author = "them"
                let finalMessage = {
                    author: author,
                    type: "text",
                    data: {
                        text: temp.message
                    }
                }
                messages.push(finalMessage);
            }
            else {
                author = "me"
            }

            this.setState({ messageList: messages })
        }
    }

    _onMessageWasSent(message) {
        const { Client1, Client2 } = this.state;
        Client1.send(JSON.stringify({
            message: message.data.text,
            from: "Client",
            client: this.context.clientId,
            invigilator: "1",
        }));
        Client2.send(JSON.stringify({
            message: message.data.text,
            from: "Client",
            client: this.context.clientId,
            invigilator: "1",
            order_id: this.props.order
        }))
        this.setState({
            messageList: [...this.state.messageList, message]
        })
    }


    componentWillUnmount() {
        const { Client1 } = this.state;
        Client1.onclose = (data) => {
            console.log(data)
        }
    }

    _sendMessage(text) {
        if (text.length > 0) {
            this.setState({
                messageList: [...this.state.messageList, {
                    author: 'them',
                    type: 'text',
                    data: { text }
                }]
            })
        }
    }

    render() {
        return (<div>
            <Launcher
                agentProfile={{
                    teamName: 'Help | Contact Us',
                    imageUrl: customerCare
                }}
                onMessageWasSent={this._onMessageWasSent.bind(this)}
                messageList={this.state.messageList}
                showEmoji={false}
            />
        </div>)
    }
}

export default ChatModal;