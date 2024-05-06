const { type } = require("os");

class Client {
  static connectToServer(client) {
    // サーバーアドレスを指定
    return new Promise((resolve, reject) => {
    const serverAddress = "socket_file";
    client.connect(serverAddress, () => {
      console.log("Connected");
      this.receiveResponse(client);
      resolve(client);
    });
  });
}

  static sendToRequest(client) {
    // リクエストを送信
    const request = RequestBuilder.buildRequest()
    .then((request) => {
      client.write(JSON.stringify(request), (err) => {
        if (err) {
          console.error("Error!! Failed to send request", err.message);
          client.end();
        } else {
          console.log("Request sent");
        }
      });
    })
    .catch((err) => {
      console.error("Error!! Failed to build request.", err.message);
      console.log("closing connection...")
      process.exit(1);
    });
  }

  static receiveResponse(client) {
    // 30秒間のタイムアウトを設定
    client.setTimeout(30000, () => {
      console.log("Connection timed out");
      client.end();
    });
    // レスポンスを受信
    client.on("data", (data) => {
      console.log("Received: " + data.toString());
    });
    // エラーが発生した場合、エラーメッセージを表示
    client.on("error", (err) => {
      console.error("Error: " + err.message);
    });
    // レスポンスを受け取ったら、ソケットを閉じる
    client.on("end", () => {
      console.log("Connection closed");
      client.end();
      process.exit(1);
    });
  }
}

class RequestBuilder {
  static buildRequest() {
    return new Promise((resolve, reject) => {
      // ユーザーからの入力を受け取り、'method', 'params', 'params_type', 'id'をJSON形式で返す
      const readline = require("readline");
      const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
      });

      let method = "";
      let params = "";
      let paramsType = "";
      let id = "";


      rl.question("Please enter the method: ", (answer) => {
        if (!answer) {
          reject(new Error('Method is required'));
          return;
        } else if (typeof answer !== "string") {
          reject(new Error("Method must be a string"));
          return;
        }
        rl.question("Please enter the params: ", (answer2) => {
          if (!answer2) {
            reject(new Error("Params is required"));
            return;
            // パラメータに','が2個以上含まれている場合、エラーを返す
          } else if (answer2.split(",").length > 2){
            reject(new Error("Invalid params.Up to two arguments are allowed."));
            return;
          }
          rl.question("Please enter the params_type: ", (answer3) => {
              method = answer;
              // パラメータを配列に変換
              params = RequestBuilder.convertParams(answer2);
              paramsType = answer3;
              id = Math.floor(Math.random() * 1000) + 1;

              const request = {
                method: method,
                params: params,
                params_type: paramsType,
                id: id,
              };

              console.log(params)
              console.log(JSON.stringify(request));
              rl.close();
              resolve(request);
          });
        });
      });
    });
  }

  // 入力されたパラメータの型により返す値を変える関数
  static convertParams(answer) {
    // パラメータが','で区切られている場合、配列に変換
    if (answer.includes(",")) {
      return answer.split(",");
    } else {
      return answer;
    }
  }
}

function main() {
  const net = require("net");
  const client = new net.Socket();
  client.setTimeout(30000);
  Client.connectToServer(client).then((client) => {
    Client.sendToRequest(client);
  });
}

main();
