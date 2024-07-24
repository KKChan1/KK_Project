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
                //����һ��ؓ؟�O ��Socket
                Socket socketWatch = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

                //����ip��ַ�Ͷ˿�̖����
                // ��һ�N ���� IPAddress ip = IPAddress.Parse(txtServer.Text); ��������
                // �ڶ��N ����
                IPAddress ip = IPAddress.Any;

                //�����˿�̖����
                IPEndPoint point = new IPEndPoint(ip, Convert.ToInt32(txtPort.Text));

                //׌ؓ؟�O ��Socket����IP��ַ���˿�̖
                socketWatch.Bind(point);

                ShowMsg("StarSocket");

                //�O�ñO ���
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
        /// �ȴ��͑��˵��B�� �K�҄����c֮ͨ���õ�Socket
        /// </summary>
        void Listen(object o)
        {
            Socket socketWatch = o as Socket;

            //ؓ؟�O ��Socket ����տ͑��˵��B�� �������͑���ͨ�ŵ�Socket
            while (true)
            {
                try
                {
                    //ؓ؟���͑���ͨ�ŵ�Socket
                    socketSend = socketWatch.Accept();

                    //���h���B�ӵĿ͑��˵�ip��ַ��Socket���뼯����
                    dicSocket.Add(socketSend.RemoteEndPoint.ToString(), socketSend);

                    //���h���B�ӵ�ip��ַ�Ͷ˿�̖������������
                    cboUsers.Items.Add(socketSend.RemoteEndPoint.ToString());

                    ShowMsg(socketSend.RemoteEndPoint.ToString() + "�B�ӳɹ�");

                    //�_��һ���¾��� ��ͣ�Ľ��տ͑��˰l���^�����Ϣ
                    Thread th = new Thread(Receive);
                    th.IsBackground = true;
                    th.Start(socketSend);
                }
                catch
                { }
            }
        }

        //���h���B�ӵĿ͑��˵�ip��ַ��Socket���뼯����
        Dictionary<string, Socket> dicSocket = new Dictionary<string, Socket>();

        /// <summary>
        /// �������˲�ͣ�Ľ��տ͑��˰l���^�����Ϣ
        /// </summary>
        /// <param name="o"></param>
        void Receive(object o)
        {
            Socket socketSend = o as Socket;
            while (true)
            {
                try
                {
                    //�͑����B�ӳɹ��� ��������ԓ���տ͑��˰l�����Ϣ
                    byte[] buffer = new byte[1024 * 1024 * 2];
                    //���H���յ�����Ч�ֹ���
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
        /// �������o�͑��˰l����Ϣ
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnSend_Click(object sender, EventArgs e)
        {
            try
            {
                string str = txtMsg.Text;
                byte[] buffer = System.Text.Encoding.UTF8.GetBytes(str);
                //��һ�����M �L�Ȟ� buffer.length+1 newBuffer[0]=0;

                List<byte> list = new List<byte>();
                list.Add(0);
                list.AddRange(buffer);
                //�����ͼ����D�Q�锵�M
                byte[] newBuffer = list.ToArray();


                //�@���Ñ������������x�е�ip��ַ
                string ip = cboUsers.SelectedItem.ToString();
                dicSocket[ip].Send(newBuffer);

                //socketSend.Send(buffer);
            }
            catch
            { }
        }

        /// <summary>
        /// �x��Ҫ�l�͵��ļ�
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void btnSelect_Click(object sender, EventArgs e)
        {
            OpenFileDialog ofd = new OpenFileDialog();
            ofd.InitialDirectory = @"C:\Users\KK Chan\Desktop";
            ofd.Title = "Ո�x��Ҫ�l�͵��ļ�";
            ofd.Filter = "�����ļ�|*.*";
            ofd.ShowDialog();

            txtPath.Text = ofd.FileName;
        }

        private void btnSendFile_Click(object sender, EventArgs e)
        {
            //���Ҫ�l�ʹ��ļ� ��Ҫ�õ� ���c�m��****(�]�W)

            //�@��Ҫ�l���ļ���·��
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
        /// �l������
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
