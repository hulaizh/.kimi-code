# Kimi reads proxy environment variables, not macOS network preferences.
kimi() (
    if [[ -z "${http_proxy}${HTTP_PROXY}${https_proxy}${HTTPS_PROXY}${all_proxy}${ALL_PROXY}" ]]; then
        local proxy_settings proxy_protocol proxy_enabled proxy_host proxy_port
        proxy_settings="$(/usr/sbin/scutil --proxy)"
        for proxy_protocol in HTTP HTTPS; do
            proxy_enabled="$(awk -v key="${proxy_protocol}Enable" '$1 == key { print $3 }' <<< "$proxy_settings")"
            proxy_host="$(awk -v key="${proxy_protocol}Proxy" '$1 == key { print $3 }' <<< "$proxy_settings")"
            proxy_port="$(awk -v key="${proxy_protocol}Port" '$1 == key { print $3 }' <<< "$proxy_settings")"
            if [[ "$proxy_enabled" == 1 && -n "$proxy_host" && "$proxy_port" == <-> ]]; then
                export "${proxy_protocol}_PROXY=http://${proxy_host}:${proxy_port}"
            fi
        done
        if [[ -n "${HTTP_PROXY}${HTTPS_PROXY}" ]]; then
            export NO_PROXY="${no_proxy:-${NO_PROXY:-localhost,127.0.0.1,::1}}"
        fi
    fi
    command kimi "$@"
)
