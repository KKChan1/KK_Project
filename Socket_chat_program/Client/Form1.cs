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
                //����ؓ؟ͨ�ŵ�Socket
                socketSend = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
                IPAddress ip = IPAddress.Parse(txtServer.Text);
                IPEndPoint point = new IPEndPoint(ip, Convert.ToInt32(txtPort.Text));
                //�@��Ҫ�B�ӵ��h�̷��������ó����ip��ַ�Ͷ˿�̖
                socketSend.Connect(point);
                ShowMsg("�B�ӳɹ�");

                //�_��һ���µľ��̲�ͣ�Ľ��շ������l�����Ϣ
                Thread th = new Thread(Recive);
                th.IsBackground = true;
                th.Start();
            }
            catch 
            { }
        }

        /// <summary>
        /// ��ͣ�Ľ��շ������l�́����Ϣ
        /// </summary>
        void Recive()
        {
            while (true)
            {
                try
                {
                    byte[] buffer = new byte[1024 * 1024 * 2];

                    //���H���յ�����Ч�ֹ���
                    int r = socketSend.Receive(buffer);
                    if (r == 0)
                    {
                        break;
                    }

                    //��ʾ�l�͵���������Ϣ
                    if (buffer[0] == 0)
                    {
                        string s = Encoding.UTF8.GetString(buffer, 1, r-1);
                        ShowMsg(socketSend.RemoteEndPoint + ":" + s);
                    }
                    else if (buffer[0] == 1)
                    {
                        SaveFileDialog sfd = new SaveFileDialog();
                        sfd.InitialDirectory = @"C:\Users\KK Chan\Desktop";
                        sfd.Title = "Ո�x��Ҫ������ļ�";
                        sfd.Filter = "�����ļ�|*.*";
                        sfd.ShowDialog(this);
                        string path = sfd.FileName;
                        using (FileStream fsWrite = new FileStream(path, FileMode.OpenOrCreate, FileAccess.ReadWrite))
                        {
                            fsWrite.Write(buffer,1,r-1);
                        }
                        MessageBox.Show("����ɹ�");
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
        /// ����
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
        /// �͑��˽o�������l����Ϣ
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
