# GitHub Release Guide

## Overview
This guide explains how to deploy your Star Wars: Rebellion Community Fix Installer to GitHub Releases. You have two options: **Manual Release** or **Automatic Release** via GitHub Actions.

## Option 1: Manual Release (Recommended for first release)

### Step 1: Prepare the Release Files
Run the release preparation script on your local machine:

```bash
python prepare_release.py
```

This will:
- Install required dependencies (PyInstaller, pywin32)
- Build the standalone Windows executable
- Create the distribution package
- Generate a ZIP file ready for upload

### Step 2: Set Up GitHub Repository
1. **Create a new repository** on GitHub (if you haven't already)
2. **Push your code** to the repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Star Wars Rebellion Community Fix Installer"
   git branch -M main
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git push -u origin main
   ```

### Step 3: Create the GitHub Release
1. Go to your GitHub repository
2. Click **"Releases"** (on the right side of the repository page)
3. Click **"Create a new release"**
4. Fill in the release details:
   - **Tag version**: `v2.63.1.0`
   - **Release title**: `Star Wars: Rebellion Community Fix v2.63.1.0`
   - **Description**: Copy the description from the workflow file
5. **Upload the ZIP file** created by the preparation script
6. Click **"Publish release"**

## Option 2: Automatic Release via GitHub Actions

### Step 1: Push Code with Workflow
The GitHub Actions workflow is already created in `.github/workflows/release.yml`. This workflow will:
- Automatically build the executable on Windows
- Create the distribution package
- Upload it as a release when you push a git tag

### Step 2: Trigger Automatic Release
Push your code and create a tag:

```bash
git add .
git commit -m "Ready for release v2.63.1.0"
git push origin main

# Create and push a tag to trigger the release
git tag v2.63.1.0
git push origin v2.63.1.0
```

The GitHub Actions workflow will automatically:
1. Build the Windows executable
2. Create the distribution package
3. Create a GitHub release with the ZIP file attached

## Release Package Contents

Your release will include:
```
Star_Wars_Rebellion_Community_Fix_v2.63.1.0.zip
├── Star_Wars_Rebellion_Community_Fix_Installer.exe
├── D3Dlmm.dll
├── d3drm.dll  
├── DDraw.dll
├── REBEXE.exe
├── README.md
├── LICENSE
└── INSTALLATION_INSTRUCTIONS.txt
```

## User Instructions (for your release description)

```markdown
## Star Wars: Rebellion Community Fix v2.63.1.0

### Features
- ✅ Automatic game detection (GOG, Steam, Original versions)  
- ✅ Safe backup creation with timestamps
- ✅ Critical shortcut modification with -w flag
- ✅ Windows XP compatibility configuration
- ✅ Steam version detection and warnings
- ✅ Complete uninstall/restore functionality

### Installation
1. Download the ZIP file below
2. Extract all files to a folder
3. Run `Star_Wars_Rebellion_Community_Fix_Installer.exe`
4. Follow the installer instructions

### System Requirements
- Windows 7/8/10/11 (32-bit or 64-bit)
- Star Wars: Rebellion (any version)
- 50MB free disk space  
- Administrator privileges (for Program Files installations)

### Files Included
- Main installer executable
- All required patch files (D3Dlmm.dll, d3drm.dll, DDraw.dll, REBEXE.exe)
- Documentation and instructions
```

## Testing Your Release

After creating the release:
1. **Download the ZIP file** from your GitHub release
2. **Extract it on a clean Windows machine**
3. **Run the installer** to verify it works correctly
4. **Test all features**: auto-detection, manual selection, installation, uninstall

## Troubleshooting

### Common Issues:
- **"Missing patch files"**: Ensure all DLL and EXE files are in your project root
- **"PyInstaller not found"**: Run `pip install pyinstaller pywin32`
- **"Build failed"**: Check that you're running on Windows or use the GitHub Actions approach

### GitHub Actions Issues:
- **Workflow not running**: Make sure the `.github/workflows/release.yml` file is pushed to your repository
- **Build fails**: Check the Actions tab in your GitHub repository for detailed error logs

## Next Steps

Once your release is published:
1. **Share the GitHub release link** with users
2. **Monitor the Issues tab** for user feedback
3. **Update the version** in your code for future releases
4. **Create new releases** by pushing new tags (e.g., `v2.63.1.1`)

## Security Note

Windows Defender may flag the executable initially (common with PyInstaller). Users can safely add it to their antivirus exceptions. For production releases, consider code signing certificates to avoid security warnings.