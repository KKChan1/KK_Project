using System.Net;
using System.Net.Sockets;
using System.Text;

namespace _06_Client
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        Socket socketSend;

        private void btnStart_Click(object sender, EventArgs e)
        {
            try
            {
                //創建負責通信的Socket
                socketSend = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
                IPAddress ip = IPAddress.Parse(txtServer.Text);
                IPEndPoint point = new IPEndPoint(ip, Convert.ToInt32(txtPort.Text));
                //獲得要連接的遠程服務器應用程序的ip地址和端口號
                socketSend.Connect(point);
                ShowMsg("連接成功");

                //開啟一個新的線程不停的接收服務器發來的消息
                Thread th = new Thread(Recive);
                th.IsBackground = true;
                th.Start();
            }
            catch 
            { }
        }

        /// <summary>
        /// 不停的接收服務器發送來的消息
        /// </summary>
        void Recive()
        {
            while (true)
            {
                try
                {
                    byte[] buffer = new byte[1024 * 1024 * 2];

                    //實際接收到的有效字節數
                    int r = socketSend.Receive(buffer);
                    if (r == 0)
                    {
                        break;
                    }

                    //表示發送的是文字消息
                    if (buffer[0] == 0)
                    {
                        string s = Encoding.UTF8.GetString(buffer, 1, r-1);
                        ShowMsg(socketSend.RemoteEndPoint + ":" + s);
                    }
                    else if (buffer[0] == 1)
                    {
                        SaveFileDialog sfd = new SaveFileDialog();
                        sfd.InitialDirectory = @"C:\Users\KK Chan\Desktop";
                        sfd.Title = "請選擇要保存的文件";
                        sfd.Filter = "所有文件|*.*";
                        sfd.ShowDialog(this);
                        string path = sfd.FileName;
                        using (FileStream fsWrite = new FileStream(path, FileMode.OpenOrCreate, FileAccess.ReadWrite))
                        {
                            fsWrite.Write(buffer,1,r-1);
                        }
                        MessageBox.Show("保存成功");
                    }
                    else if (buffer[0] == 2)
                    {
                        ZD();
                    }
                }
                catch 
                { }
            }
        }

        /// <summary>
        /// 震動
        /// </summary>
        void ZD()
        {
            for (int i = 0; i < 500; i++)
            {
                this.Location = new Point(200,200);
                this.Location = new Point(280, 280);
            }
        }

        void ShowMsg(string str)
        {
            txtLog.AppendText(str + "\r\n");
        }

        /// <summary>
        /// 客戶端給服務器發送信息
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnSend_Click(object sender, EventArgs e)
        {
            string str = txtMsg.Text.Trim();
            byte[] buffer = System.Text.Encoding.UTF8.GetBytes(str);
            socketSend.Send(buffer);
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            Control.CheckForIllegalCrossThreadCalls = false;
        }
    }
}
