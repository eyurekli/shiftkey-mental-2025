import "../styles/Header.css";

export default function Header()
{
    return (
        <>
            <header>
                <h1>Calmora</h1>
                <div id="links">
                    <h3><a href="https://www.github.com" target="_blank">About Us</a></h3>
                    <button id="mode-switch">Dark Mode</button>
                </div>
            </header>
        </>
    )
}