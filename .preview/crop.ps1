Add-Type -AssemblyName System.Drawing
function Save-Crop($file, $x, $y, $w, $h, $path) {
  $img = [System.Drawing.Bitmap]::FromFile($file)
  $bmp = New-Object System.Drawing.Bitmap $w, $h
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $dest = New-Object System.Drawing.Rectangle 0, 0, $w, $h
  $rect = New-Object System.Drawing.Rectangle $x, $y, $w, $h
  $g.DrawImage($img, $dest, $rect, [System.Drawing.GraphicsUnit]::Pixel)
  $bmp.Save($path, [System.Drawing.Imaging.ImageFormat]::Jpeg)
  $g.Dispose(); $bmp.Dispose(); $img.Dispose()
}
Save-Crop 'c:\gitreps\perinatal-trauma\.preview\desktop-900.png' 860 65 580 835 'c:\gitreps\perinatal-trauma\.preview\face.jpg'
Write-Host 'ok'
