using Microsoft.VisualBasic;
using Newtonsoft.Json;
using System.Diagnostics;
using System.IO.Compression;
using System.Net;
using System.Net.Http.Headers;

namespace update
{
    public partial class Form1 : Form
    {
        private string latestVersion = null;
        private string JsonVersion = null;
        private string updatefilesize = null;
        private double TotalSize = 0;
        private double TotalSizeMB = 0;
        private double getdownloadedSize = 0;

        public Form1()
        {
            InitializeComponent();
            this.FormClosing += cancel_btn_Click;

        }

        private void Form1_Load(object sender, EventArgs e)
        {
            GetTagNameFromApi();
        }

        public void DownloadFileWithProgress()
        {
            string zipUrl = $"https://github.com/nsblollipop/NSBotUpdate/releases/download/{latestVersion}/NSBotUpdate.zip";
            string zipFileName = "NSBotUpdate.zip";
            string totalFileSizeString = updatefilesize;
            double totalFileSize;
            if (double.TryParse(totalFileSizeString, out totalFileSize))
            {
                double totalSizeMB = totalFileSize / (1024.0 * 1024.0);
                double roundedTotalSizeMB = Math.Round(totalSizeMB, 3);
                this.TotalSize = totalFileSize;
                this.TotalSizeMB = roundedTotalSizeMB;
            }
            else
            {
                // จัดการกรณีไม่สามารถแปลงขนาดไฟล์เป็นตัวเลขได้
            }

            using (System.Windows.Forms.Timer timer = new System.Windows.Forms.Timer())
            {
                timer.Interval = 300; // อัพเดตทุกๆ 300ms
                timer.Tick += (sender, e) =>
                {
                    UpdateProgress();
                };

                using (WebClient client = new WebClient())
                {
                    client.DownloadProgressChanged += (sender, e) =>
                    {
                        this.getdownloadedSize = e.BytesReceived;
                        timer.Start(); // เริ่มต้น Timer เมื่อเริ่มรับข้อมูล

                    };

                    client.DownloadFileCompleted += (sender, e) =>
                    {
                        double progressPercentage = (totalFileSize / totalFileSize) * 100;
                        progressBar.Value = (int)progressPercentage;
                        process_label.Text = $"Download complete..";
                        timer.Stop(); // หยุด Timer เมื่อดาวน์โหลดเสร็จสิ้น
                        if (e.Error == null)
                        {
                            // ดาวน์โหลดเสร็จสิ้น
                            Extract_file();
                        }
                        else
                        {
                            // เกิดข้อผิดพลาดในการดาวน์โหลด
                            Console.WriteLine($"Error downloading file: {e.Error.Message}");
                        }
                    };

                    try
                    {
                        // เริ่มดาวน์โหลดไฟล์
                        client.DownloadFileAsync(new Uri(zipUrl), zipFileName);
                    }
                    catch (WebException ex)
                    {
                        // จัดการข้อผิดพลาดที่เกิดขึ้นในการดาวน์โหลด
                    }
                    catch (Exception ex)
                    {
                        // จัดการข้อผิดพลาดที่ไม่ได้เกี่ยวข้องกับการดาวน์โหลด
                    }
                }
            }
        }

        private void UpdateProgress()
        {
            double downloadedSizeMB = getdownloadedSize / (1024.0 * 1024.0);
            double progressPercentage = (getdownloadedSize / TotalSize) * 100;
            double roundedDownloadedSizeMB = Math.Round(downloadedSizeMB, 3);

            progressBar.Value = (int)progressPercentage;
            process_label.Text = $"Downloading {(int)progressPercentage}% ({roundedDownloadedSizeMB} of {TotalSizeMB} MB)...";
        }


        private async void Extract_file()
        {
            string zipFilePath = "NSBotUpdate.zip";
            string extractPath = "ExtractedFiles";
            process_label.Text = $"Extracting {zipFilePath}";

            try
            {
                // ตรวจสอบว่ามีไดเรกทอรี extractPath อยู่หรือไม่
                if (Directory.Exists(extractPath))
                {
                    // ลบไดเรกทอรีที่มีอยู่ใน extractPath และไฟล์ที่อยู่ภายใน
                    Directory.Delete(extractPath, true);
                }

                await Task.Run(() =>
                {
                    // แตกไฟล์ ZIP
                    DeleteFilesInProgramFolder();
                    ZipFile.ExtractToDirectory(zipFilePath, extractPath);
                    MoveFilesFromExtractedFolder();
                });

            }
            catch (Exception ex)
            {
                // เกิดข้อผิดพลาดในการแตกไฟล์
                MessageBox.Show("Error extracting file: " + ex.Message);
            }
        }


        private void DeleteFilesInProgramFolder()
        {
            string programFolderPath = AppDomain.CurrentDomain.BaseDirectory;
            process_label.Text = "Remove old file..";

            DeleteFilesRecursively(programFolderPath);
        }

        private void DeleteFilesRecursively(string folderPath)
        {
            foreach (string filePath in Directory.GetFiles(folderPath))
            {
                string fileName = Path.GetFileName(filePath);

                if (fileName != "runupdate.exe" && fileName != "NSBotUpdate.zip")
                {
                    File.Delete(filePath);
                }
            }

            foreach (string subFolderPath in Directory.GetDirectories(folderPath))
            {
                DeleteFilesRecursively(subFolderPath);
                Directory.Delete(subFolderPath);
            }
        }


        private void MoveFilesFromExtractedFolder()
        {
            process_label.Text = $"Move file to folder..";
            string extractPath = "ExtractedFiles";
            string programFolderPath = AppDomain.CurrentDomain.BaseDirectory;

            // ตรวจสอบว่ามีไดเรกทอรี extractPath อยู่หรือไม่
            if (Directory.Exists(extractPath))
            {
                // หาไฟล์และโฟลเดอร์ทั้งหมดภายใน extractPath รวมถึงโฟลเดอร์ย่อย
                string[] allFiles = Directory.GetFiles(extractPath, "*", SearchOption.AllDirectories);

                // ย้ายไฟล์และโฟลเดอร์ทั้งหมดไปยังโฟลเดอร์ปลายทาง
                foreach (string filePath in allFiles)
                {
                    string relativePath = filePath.Substring(extractPath.Length + 1);
                    string destinationFilePath = Path.Combine(programFolderPath, relativePath);

                    // ตรวจสอบว่าเป็นไฟล์หรือโฟลเดอร์
                    if (File.Exists(filePath))
                    {
                        // ย้ายไฟล์
                        string destinationDirectory = Path.GetDirectoryName(destinationFilePath);
                        Directory.CreateDirectory(destinationDirectory);
                        File.Move(filePath, destinationFilePath);
                    }
                    else if (Directory.Exists(filePath))
                    {
                        // สร้างโฟลเดอร์ปลายทาง
                        Directory.CreateDirectory(destinationFilePath);
                    }
                }

                // ลบโฟลเดอร์ extractPath
                Directory.Delete(extractPath, true);
                OpenNSLaunch();
                OnClosing();
            }
        }
        private void OpenNSLaunch()
        {
            string programFolderPath = AppDomain.CurrentDomain.BaseDirectory;
            string nsLaunchPath = Path.Combine(programFolderPath, "NSLaunch.exe");

            if (File.Exists(nsLaunchPath))
            {
                try
                {
                    Process.Start(nsLaunchPath);
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Error opening NSLaunch.exe: " + ex.Message);
                }
            }
            else
            {
                MessageBox.Show("NSLaunch.exe not found.");
            }
        }


        //==============================================Get API===============================================
        private async void GetTagNameFromApi()
        {
            string apiUrl = "https://api.github.com/repos/nsblollipop/NSBotUpdate/releases/latest";
            string token = "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"; // แทนที่ด้วย Token ของ API

            HttpClient client = new HttpClient();
            client.DefaultRequestHeaders.UserAgent.ParseAdd("Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)");

            try
            {
                HttpResponseMessage response = await GetApiResponse(client, apiUrl, token);

                if (response.IsSuccessStatusCode)
                {
                    //MessageBox.Show("With token!");
                    string responseContent = await response.Content.ReadAsStringAsync();
                    dynamic jsonResponse = JsonConvert.DeserializeObject(responseContent);
                    string tagName = jsonResponse["tag_name"];
                    string size = jsonResponse["assets"][0]["size"];
                    this.latestVersion = tagName;
                    this.updatefilesize = size;
                }
                else
                {
                    //MessageBox.Show("Without token!");
                    HttpResponseMessage responseWithoutToken = await GetApiResponse(client, apiUrl, null);
                    string responseContent = await responseWithoutToken.Content.ReadAsStringAsync();
                    dynamic jsonResponse = JsonConvert.DeserializeObject(responseContent);
                    string tagName = jsonResponse["tag_name"];
                    string size = jsonResponse["assets"][0]["size"];
                    this.latestVersion = tagName;
                    this.updatefilesize = size;
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error retrieving tag name from API: " + ex.Message);
                this.latestVersion = JsonVersion;
            }
            process_label.Text = $"latest version {latestVersion}";
            DownloadFileWithProgress();

        }

        private async Task<HttpResponseMessage> GetApiResponse(HttpClient client, string apiUrl, string token)
        {
            if (!string.IsNullOrEmpty(token))
            {
                client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
            }
            else
            {
                client.DefaultRequestHeaders.Authorization = null;
            }

            return await client.GetAsync(apiUrl);
        }

        private void cancel_btn_Click(object sender, EventArgs e)
        {
            OnClosing();
        }

        private void OnClosing()
        {
            try
            {
                string fileName = "rmzip.bat";
                string fileContent = "@echo off\necho Waiting for 2 seconds...\ntimeout /t 2 >nul\nrd /s /q ExtractedFiles\ndel NSBotUpdate.zip\nren runupdate.exe update.exe\ndel rmzip.bat";

                using (StreamWriter writer = new StreamWriter(fileName))
                {
                    writer.Write(fileContent);
                }
            }
            catch (Exception)
            {
                // จัดการข้อผิดพลาดที่เกิดขึ้นในการสร้างไฟล์
            }

            Process.Start(new ProcessStartInfo()
            {
                FileName = "rmzip.bat",
                CreateNoWindow = true,
                UseShellExecute = false
            });

            Application.Exit();
        }


        //====================================================================================================
    }
}