#!/bin/bash

main() {
    clear
    echo -e "Welcome to the MacSploit Experience!"
    echo -e "Install Script Version 2.3"

    echo -ne "Checking License..."
    curl -s "https://git.abyssdigital.xyz/main/jq-macos-amd64" -o "./jq"
    chmod +x ./jq
    
    curl -s "https://git.abyssdigital.xyz/sellix/hwid" -o "./hwid"
    chmod +x ./hwid
    
    local user_hwid=$(./hwid)
    local hwid_resp=$(curl -s "https://git.abyssdigital.xyz/api/whitelist?hwid=$user_hwid" | ./jq -r ".success")
    rm ./hwid
    
    echo -e " Done.\nWhitelist Status Verified."

    echo -e "Downloading Latest Roblox..."
    [ -f ./RobloxPlayer.zip ] && rm ./RobloxPlayer.zip
    local version=$(curl -s "https://clientsettingscdn.roblox.com/v2/client-version/MacPlayer" | ./jq -r ".clientVersionUpload")
    curl "http://setup.rbxcdn.com/mac/$version-RobloxPlayer.zip" -o "./RobloxPlayer.zip"
    rm ./jq

    echo -n "Installing Latest Roblox... "
    [ -d "/Applications/Roblox.app" ] && rm -rf "/Applications/Roblox.app"
    unzip -o -q "./RobloxPlayer.zip"
    mv ./RobloxPlayer.app /Applications/Roblox.app
    rm ./RobloxPlayer.zip
    echo -e "Done."

    echo -e "Downloading MacSploit..."
    curl "https://git.abyssdigital.xyz/main/macsploit.zip" -o "./MacSploit.zip"

    echo -n "Installing MacSploit... "
    unzip -o -q "./MacSploit.zip"
    echo -e "Done."

    echo -n "Updating Dylib..."
    if [ "$version" == "version-88b4e5cd14654499" ]
    then
        curl -Os "https://git.abyssdigital.xyz/preview/macsploit.dylib"
    else
        curl -Os "https://git.abyssdigital.xyz/main/macsploit.dylib"
    fi
    
    echo -e " Done."
    echo -e "Patching Roblox..."
    mv ./macsploit.dylib "/Applications/Roblox.app/Contents/MacOS/macsploit.dylib"
    mv ./libdiscord-rpc.dylib "/Applications/Roblox.app/Contents/MacOS/libdiscord-rpc.dylib"
    ./insert_dylib "/Applications/Roblox.app/Contents/MacOS/macsploit.dylib" "/Applications/Roblox.app/Contents/MacOS/RobloxPlayer" --strip-codesig --all-yes
    mv "/Applications/Roblox.app/Contents/MacOS/RobloxPlayer_patched" "/Applications/Roblox.app/Contents/MacOS/RobloxPlayer"
    rm -r "/Applications/Roblox.app/Contents/MacOS/RobloxPlayerInstaller.app"
    rm ./insert_dylib

    echo -n "Installing MacSploit App... "
    [ -d "/Applications/MacSploit.app" ] && rm -rf "/Applications/MacSploit.app"
    mv ./MacSploit.app /Applications/MacSploit.app
    rm ./MacSploit.zip
    echo -e "Done."

    echo -e "Install Complete! Developed by Nexus42!"
    exit
}

main
