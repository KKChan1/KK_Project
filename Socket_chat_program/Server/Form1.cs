using System.Net;
using System.Net.Sockets;
using System.Text;

namespace _06_Server
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            try
            {
                //創建一個負責監聽的Socket
                Socket socketWatch = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

                //創建ip地址和端口號對象
                // 第一種 方法 IPAddress ip = IPAddress.Parse(txtServer.Text); 但會寫死
                // 第二種 方法
                IPAddress ip = IPAddress.Any;

                //創建端口號對象
                IPEndPoint point = new IPEndPoint(ip, Convert.ToInt32(txtPort.Text));

                //讓負責監聽的Socket綁定IP地址跟端口號
                socketWatch.Bind(point);

                ShowMsg("StarSocket");

                //設置監聽隊列
                socketWatch.Listen(10);

                Thread th = new Thread(Listen);
                th.IsBackground = true;
                th.Start(socketWatch);
            }
            catch
            { }
        }

        Socket socketSend;

        /// <summary>
        /// 等待客戶端的連接 並且創建與之通信用的Socket
        /// </summary>
        void Listen(object o)
        {
            Socket socketWatch = o as Socket;

            //負責監聽的Socket 來接收客戶端的連接 創建跟客戶端通信的Socket
            while (true)
            {
                try
                {
                    //負責跟客戶端通信的Socket
                    socketSend = socketWatch.Accept();

                    //將遠程連接的客戶端的ip地址和Socket存入集合中
                    dicSocket.Add(socketSend.RemoteEndPoint.ToString(), socketSend);

                    //將遠程連接的ip地址和端口號存入下拉框中
                    cboUsers.Items.Add(socketSend.RemoteEndPoint.ToString());

                    ShowMsg(socketSend.RemoteEndPoint.ToString() + "連接成功");

                    //開啟一個新線程 不停的接收客戶端發送過來的消息
                    Thread th = new Thread(Receive);
                    th.IsBackground = true;
                    th.Start(socketSend);
                }
                catch
                { }
            }
        }

        //將遠程連接的客戶端的ip地址和Socket存入集合中
        Dictionary<string, Socket> dicSocket = new Dictionary<string, Socket>();

        /// <summary>
        /// 服務器端不停的接收客戶端發送過來的消息
        /// </summary>
        /// <param name="o"></param>
        void Receive(object o)
        {
            Socket socketSend = o as Socket;
            while (true)
            {
                try
                {
                    //客戶端連接成功後 服務器應該接收客戶端發來的消息
                    byte[] buffer = new byte[1024 * 1024 * 2];
                    //實際接收到的有效字節數
                    int r = socketSend.Receive(buffer);
                    if (r == 0)
                    {
                        break;
                    }
                    string str = Encoding.UTF8.GetString(buffer, 0, r);
                    ShowMsg(socketSend.RemoteEndPoint + ":" + str);
                }
                catch
                { }
            }
        }

        void ShowMsg(string str)
        {
            txtLog.AppendText(str + "\r\n");
        }


        private void Form1_Load(object sender, EventArgs e)
        {
            Control.CheckForIllegalCrossThreadCalls = false;
        }

        /// <summary>
        /// 服務器給客戶端發送消息
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnSend_Click(object sender, EventArgs e)
        {
            try
            {
                string str = txtMsg.Text;
                byte[] buffer = System.Text.Encoding.UTF8.GetBytes(str);
                //聲明一個新數組 長度為 buffer.length+1 newBuffer[0]=0;

                List<byte> list = new List<byte>();
                list.Add(0);
                list.AddRange(buffer);
                //將泛型集合轉換為數組
                byte[] newBuffer = list.ToArray();


                //獲得用戶在下拉框中選中的ip地址
                string ip = cboUsers.SelectedItem.ToString();
                dicSocket[ip].Send(newBuffer);

                //socketSend.Send(buffer);
            }
            catch
            { }
        }

        /// <summary>
        /// 選擇要發送的文件
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnSelect_Click(object sender, EventArgs e)
        {
            OpenFileDialog ofd = new OpenFileDialog();
            ofd.InitialDirectory = @"C:\Users\KK Chan\Desktop";
            ofd.Title = "請選擇要發送的文件";
            ofd.Filter = "所有文件|*.*";
            ofd.ShowDialog();

            txtPath.Text = ofd.FileName;
        }

        private void btnSendFile_Click(object sender, EventArgs e)
        {
            //如果要發送大文件 需要用到 斷點續傳****(沒學)

            //獲得要發送文件的路徑
            string path = txtPath.Text;
            using (FileStream fsRead = new FileStream(path, FileMode.OpenOrCreate, FileAccess.ReadWrite))
            {
                byte[] buffer = new byte[1024 * 1024 * 5];
                int r = fsRead.Read(buffer, 0, buffer.Length);
                List<byte> list = new List<byte>();
                list.Add(1);
                list.AddRange(buffer);
                byte[] newBuffer = list.ToArray();
                dicSocket[cboUsers.SelectedItem.ToString()].Send(newBuffer, 0, r + 1, SocketFlags.None);
            }
;
        }

        /// <summary>
        /// 發送震動
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnZD_Click(object sender, EventArgs e)
        {
            byte[] buffer = new byte[1];
            buffer[0] = 2;
            dicSocket[cboUsers.SelectedItem.ToString()].Send(buffer);
        }
    }
}
